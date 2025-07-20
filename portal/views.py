from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from datetime import timedelta
import json

from .models import UserProfile, PortalSession
from .unifi_service import UniFiController


def index(request):
    """Landing page with OAuth login options"""
    # Check if user came from UniFi captive portal
    mac_address = request.GET.get('id')
    ap_mac = request.GET.get('ap')
    t = request.GET.get('t')
    url = request.GET.get('url')
    
    # Store UniFi parameters in session
    if mac_address:
        request.session['unifi_mac'] = mac_address
        request.session['unifi_ap'] = ap_mac
        request.session['unifi_t'] = t
        request.session['unifi_url'] = url
    
    context = {
        'from_unifi': bool(mac_address),
        'mac_address': mac_address,
    }
    
    return render(request, 'portal/index.html', context)


@login_required
def role_selection(request):
    """Role selection page after OAuth login"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        
        if role in ['member', 'guest', 'event']:
            profile.role = role
            
            if role == 'member':
                floor = request.POST.get('floor')
                if floor in ['1', '2', '3', '4', '5']:
                    profile.floor = floor
                else:
                    messages.error(request, 'Please select a valid floor.')
                    return render(request, 'portal/role_selection.html', {'profile': profile})
            
            elif role == 'guest':
                member_name = request.POST.get('member_name')
                if member_name:
                    profile.member_name = member_name
                else:
                    messages.error(request, 'Please enter the member name you are visiting.')
                    return render(request, 'portal/role_selection.html', {'profile': profile})
            
            elif role == 'event':
                event_name = request.POST.get('event_name')
                if event_name:
                    profile.event_name = event_name
                else:
                    messages.error(request, 'Please enter the event name.')
                    return render(request, 'portal/role_selection.html', {'profile': profile})
            
            profile.save()
            return redirect('portal:authorize')
        
        else:
            messages.error(request, 'Please select a valid role.')
    
    return render(request, 'portal/role_selection.html', {'profile': profile})


@login_required
def authorize(request):
    """Authorize user with UniFi controller"""
    mac_address = request.session.get('unifi_mac')
    
    if not mac_address:
        messages.error(request, 'No device MAC address found. Please access through the captive portal.')
        return redirect('portal:index')
    
    try:
        profile = request.user.userprofile
        if not profile.role:
            messages.error(request, 'Please select your role first.')
            return redirect('portal:role_selection')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found. Please complete role selection.')
        return redirect('portal:role_selection')
    
    # Create or update portal session
    session, created = PortalSession.objects.get_or_create(
        user=request.user,
        mac_address=mac_address,
        defaults={
            'ip_address': get_client_ip(request),
            'status': 'pending'
        }
    )
    
    # Authorize with UniFi controller
    unifi = UniFiController()
    success = unifi.authorize_guest(mac_address, duration_minutes=240)  # 4 hours
    
    if success:
        session.status = 'authorized'
        session.authorized_at = timezone.now()
        session.expires_at = timezone.now() + timedelta(hours=4)
        session.save()
        
        # Redirect to original URL or success page
        original_url = request.session.get('unifi_url')
        if original_url:
            return redirect(original_url)
        else:
            return render(request, 'portal/success.html', {
                'profile': profile,
                'session': session
            })
    else:
        session.status = 'denied'
        session.save()
        messages.error(request, 'Failed to authorize device. Please contact support.')
        return render(request, 'portal/error.html')


def auth_error(request):
    """OAuth authentication error page"""
    return render(request, 'portal/auth_error.html')


def logout_view(request):
    """Logout and redirect to index"""
    logout(request)
    return redirect('portal:index')


@csrf_exempt
def unifi_webhook(request):
    """Webhook endpoint for UniFi controller events"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Handle UniFi events here
            # This could be used to track device connections/disconnections
            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

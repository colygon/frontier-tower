from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for captive portal users"""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('guest', 'Guest'),
        ('event', 'Event Attendee'),
    ]
    
    FLOOR_CHOICES = [
        ('1', 'Floor 1'),
        ('2', 'Floor 2'),
        ('3', 'Floor 3'),
        ('4', 'Floor 4'),
        ('5', 'Floor 5'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    oauth_provider = models.CharField(max_length=50, blank=True)
    oauth_uid = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    floor = models.CharField(max_length=2, choices=FLOOR_CHOICES, blank=True)
    member_name = models.CharField(max_length=100, blank=True, help_text="For guests: name of member they're visiting")
    event_name = models.CharField(max_length=100, blank=True, help_text="For event attendees: event name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"


class PortalSession(models.Model):
    """Track user sessions for captive portal"""
    STATUS_CHOICES = [
        ('pending', 'Pending Authorization'),
        ('authorized', 'Authorized'),
        ('expired', 'Expired'),
        ('denied', 'Denied'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17, help_text="Device MAC address")
    ip_address = models.GenericIPAddressField()
    unifi_session_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    authorized_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.mac_address} - {self.status}"
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class UniFiController(models.Model):
    """UniFi Controller configuration"""
    name = models.CharField(max_length=100)
    url = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Should be encrypted in production
    site_id = models.CharField(max_length=50, default='default')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

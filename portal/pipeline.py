from .models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    """
    Save user profile information from OAuth provider
    """
    if user and backend:
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'oauth_provider': backend.name,
                'oauth_uid': response.get('sub') or response.get('id', ''),
            }
        )
        
        if not created:
            # Update existing profile
            profile.oauth_provider = backend.name
            profile.oauth_uid = response.get('sub') or response.get('id', '')
            profile.save()
    
    return {'user': user, 'profile': profile if 'profile' in locals() else None}

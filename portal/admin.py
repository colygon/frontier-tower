from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, PortalSession, UniFiController


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('oauth_provider', 'oauth_uid', 'role', 'floor', 'member_name', 'event_name')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__role')
    
    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'floor', 'oauth_provider', 'created_at')
    list_filter = ('role', 'floor', 'oauth_provider', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'member_name', 'event_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'oauth_provider', 'oauth_uid')
        }),
        ('Role & Access', {
            'fields': ('role', 'floor', 'member_name', 'event_name')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PortalSession)
class PortalSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'mac_address', 'ip_address', 'status', 'authorized_at', 'expires_at', 'is_expired')
    list_filter = ('status', 'authorized_at', 'expires_at', 'created_at')
    search_fields = ('user__email', 'mac_address', 'ip_address')
    readonly_fields = ('created_at', 'is_expired')
    
    fieldsets = (
        ('Session Information', {
            'fields': ('user', 'mac_address', 'ip_address', 'unifi_session_id')
        }),
        ('Authorization', {
            'fields': ('status', 'authorized_at', 'expires_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'is_expired'),
            'classes': ('collapse',)
        })
    )
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


@admin.register(UniFiController)
class UniFiControllerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'username', 'site_id', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'url', 'username')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Controller Information', {
            'fields': ('name', 'url', 'site_id', 'is_active')
        }),
        ('Authentication', {
            'fields': ('username', 'password'),
            'description': 'Note: Password should be encrypted in production'
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

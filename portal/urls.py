from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('role-selection/', views.role_selection, name='role_selection'),
    path('authorize/', views.authorize, name='authorize'),
    path('auth/error/', views.auth_error, name='auth_error'),
    path('logout/', views.logout_view, name='logout'),
    path('webhook/unifi/', views.unifi_webhook, name='unifi_webhook'),
]

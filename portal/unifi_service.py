import requests
import json
from django.conf import settings
from datetime import datetime, timedelta
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UniFiController:
    """UniFi Controller API client"""
    
    def __init__(self, base_url=None, username=None, password=None, site_id=None):
        self.base_url = base_url or settings.UNIFI_CONTROLLER_URL
        self.username = username or settings.UNIFI_USERNAME
        self.password = password or settings.UNIFI_PASSWORD
        self.site_id = site_id or settings.UNIFI_SITE_ID
        self.session = requests.Session()
        self.session.verify = False  # For self-signed certificates
        self.cookies = None
        
    def login(self):
        """Login to UniFi controller"""
        login_url = f"{self.base_url}/api/login"
        login_data = {
            'username': self.username,
            'password': self.password
        }
        
        try:
            response = self.session.post(login_url, json=login_data)
            response.raise_for_status()
            self.cookies = response.cookies
            return True
        except requests.exceptions.RequestException as e:
            print(f"UniFi login failed: {e}")
            return False
    
    def logout(self):
        """Logout from UniFi controller"""
        logout_url = f"{self.base_url}/api/logout"
        try:
            self.session.post(logout_url, cookies=self.cookies)
        except requests.exceptions.RequestException:
            pass
    
    def authorize_guest(self, mac_address, duration_minutes=60):
        """Authorize a guest device"""
        if not self.login():
            return False
            
        authorize_url = f"{self.base_url}/api/s/{self.site_id}/cmd/stamgr"
        
        # Calculate expiration time
        expire_time = int((datetime.now() + timedelta(minutes=duration_minutes)).timestamp() * 1000)
        
        authorize_data = {
            'cmd': 'authorize-guest',
            'mac': mac_address.lower().replace(':', ''),
            'minutes': duration_minutes,
            'up': 0,  # Upload limit (0 = unlimited)
            'down': 0,  # Download limit (0 = unlimited)
            'bytes': 0,  # Data limit (0 = unlimited)
            'ap_mac': None
        }
        
        try:
            response = self.session.post(
                authorize_url, 
                json=authorize_data, 
                cookies=self.cookies
            )
            response.raise_for_status()
            result = response.json()
            
            self.logout()
            return result.get('meta', {}).get('rc') == 'ok'
            
        except requests.exceptions.RequestException as e:
            print(f"UniFi authorization failed: {e}")
            self.logout()
            return False
    
    def unauthorize_guest(self, mac_address):
        """Unauthorize a guest device"""
        if not self.login():
            return False
            
        unauthorize_url = f"{self.base_url}/api/s/{self.site_id}/cmd/stamgr"
        
        unauthorize_data = {
            'cmd': 'unauthorize-guest',
            'mac': mac_address.lower().replace(':', '')
        }
        
        try:
            response = self.session.post(
                unauthorize_url, 
                json=unauthorize_data, 
                cookies=self.cookies
            )
            response.raise_for_status()
            result = response.json()
            
            self.logout()
            return result.get('meta', {}).get('rc') == 'ok'
            
        except requests.exceptions.RequestException as e:
            print(f"UniFi unauthorization failed: {e}")
            self.logout()
            return False
    
    def get_guest_status(self, mac_address):
        """Get guest authorization status"""
        if not self.login():
            return None
            
        guests_url = f"{self.base_url}/api/s/{self.site_id}/stat/guest"
        
        try:
            response = self.session.get(guests_url, cookies=self.cookies)
            response.raise_for_status()
            result = response.json()
            
            guests = result.get('data', [])
            for guest in guests:
                if guest.get('mac', '').lower() == mac_address.lower().replace(':', ''):
                    self.logout()
                    return guest
            
            self.logout()
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"UniFi guest status check failed: {e}")
            self.logout()
            return None

from social_core.backends.oauth import BaseOAuth2


class GovBrOAuth2(BaseOAuth2):
    """Gov.br OAuth2 authentication backend"""
    name = 'govbr'
    AUTHORIZATION_URL = 'https://sso.acesso.gov.br/authorize'
    ACCESS_TOKEN_URL = 'https://sso.acesso.gov.br/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ' '
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires'),
        ('refresh_token', 'refresh_token'),
    ]

    def get_user_details(self, response):
        """Return user details from Gov.br account"""
        return {
            'username': response.get('sub'),
            'email': response.get('email'),
            'first_name': response.get('given_name', ''),
            'last_name': response.get('family_name', ''),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://sso.acesso.gov.br/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        return self.get_json(url, headers=headers)

    def get_user_id(self, details, response):
        """Return a unique ID for the current user"""
        return response.get('sub')

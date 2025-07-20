# 🔐 Frontier Tower — Django Portal with OAuth

A Django-based captive portal for UniFi networks with OAuth authentication support. This portal replaces traditional manual forms with secure OAuth flows from providers like Google, Microsoft Azure AD, Auth0, and Gov.br.

## ✨ Features

- **OAuth Authentication**: Support for multiple OAuth providers
  - Google OAuth2
  - Microsoft Azure AD
  - Auth0
  - Gov.br (Brazil)
- **Role-Based Access**: Three user types with different requirements
  - **Members**: Select floor access
  - **Guests**: Specify member they're visiting
  - **Event Attendees**: Enter event name
- **UniFi Integration**: Direct API integration with UniFi controllers
- **Session Management**: Track and manage user sessions with expiration
- **Modern UI**: Responsive design with Bootstrap 5
- **Admin Interface**: Django admin for user and session management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- UniFi Controller (for production)
- OAuth provider credentials

### Installation

1. **Clone and setup the project:**
   ```bash
   cd /Users/colinlowenberg/CascadeProjects/frontier-tower
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your OAuth and UniFi credentials
   ```

3. **Run migrations and create superuser:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the portal:**
   - Portal: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 🔧 Configuration

### OAuth Providers

Configure your OAuth providers in the `.env` file:

#### Google OAuth2
```env
GOOGLE_OAUTH2_KEY=your-google-client-id
GOOGLE_OAUTH2_SECRET=your-google-client-secret
```

#### Microsoft Azure AD
```env
AZURE_AD_CLIENT_ID=your-azure-client-id
AZURE_AD_CLIENT_SECRET=your-azure-client-secret
AZURE_AD_TENANT_ID=your-azure-tenant-id
```

#### Auth0
```env
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
```

#### Gov.br (Brazil)
```env
GOVBR_CLIENT_ID=your-govbr-client-id
GOVBR_CLIENT_SECRET=your-govbr-client-secret
```

### UniFi Controller

Configure your UniFi controller settings:

```env
UNIFI_CONTROLLER_URL=https://your-unifi-controller:8443
UNIFI_USERNAME=your-unifi-username
UNIFI_PASSWORD=your-unifi-password
UNIFI_SITE_ID=default
```

## 🔄 User Flow

1. **UniFi Redirect**: User connects to WiFi and is redirected to portal
2. **OAuth Login**: User selects OAuth provider and authenticates
3. **Role Selection**: User selects their role and provides required information
4. **Authorization**: System authorizes device with UniFi controller
5. **Access Granted**: User gets internet access and confirmation page

## 🏗️ Architecture

### Models

- **UserProfile**: Extended user information with OAuth details and role
- **PortalSession**: Track user sessions with MAC addresses and expiration
- **UniFiController**: Configuration for UniFi controller connections

### Views

- **index**: Landing page with OAuth login options
- **role_selection**: Post-login role and information collection
- **authorize**: UniFi authorization and session creation
- **success/error**: Result pages with session information

### OAuth Backends

- Custom Gov.br OAuth2 backend
- Integration with social-auth-app-django for other providers

## 🔒 Security Features

- **OAuth-only authentication**: No manual password entry
- **Session expiration**: Automatic session timeout
- **CSRF protection**: Django CSRF middleware
- **CORS configuration**: Controlled cross-origin requests
- **Secure session handling**: HttpOnly cookies and secure flags

## 🛠️ UniFi Integration

The portal integrates directly with UniFi controllers using the REST API:

- **Guest Authorization**: Authorize devices for internet access
- **Session Management**: Track authorized devices and expiration
- **Automatic Cleanup**: Handle session expiration and cleanup

### UniFi Captive Portal Setup

1. Configure your UniFi controller's captive portal
2. Set the portal URL to your Django application
3. Configure the redirect URL format: `http://your-portal/?id={client_mac}&ap={ap_mac}&t={t}&url={url}`

## 📊 Admin Interface

Access the Django admin at `/admin/` to manage:

- **Users and Profiles**: View user information and roles
- **Portal Sessions**: Monitor active and expired sessions
- **UniFi Controllers**: Manage controller configurations

## 🚀 Production Deployment

### Environment Variables

Ensure all production environment variables are set:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
```

### Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Secret Key**: Use a strong, unique secret key
3. **Database**: Use PostgreSQL or MySQL instead of SQLite
4. **OAuth Credentials**: Keep OAuth secrets secure
5. **UniFi Credentials**: Encrypt UniFi controller passwords

### Web Server

Deploy with a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn frontier_tower.wsgi:application
```

## 🔧 Customization

### Adding OAuth Providers

1. Install the appropriate social-auth backend
2. Add the backend to `AUTHENTICATION_BACKENDS` in settings
3. Configure the provider credentials in `.env`
4. Add the login button to the index template

### Customizing User Roles

Modify the `UserProfile.ROLE_CHOICES` in `models.py` and update the role selection template accordingly.

### Styling

The portal uses Bootstrap 5 with custom CSS. Modify the styles in `templates/portal/base.html` or create separate CSS files.

## 📝 API Endpoints

- `/`: Main portal landing page
- `/role-selection/`: Role selection form
- `/authorize/`: Device authorization
- `/auth/`: Social auth URLs (login/logout)
- `/webhook/unifi/`: UniFi webhook endpoint
- `/admin/`: Django admin interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the Django documentation
- Review UniFi controller documentation
- Contact your system administrator

## 🙏 Acknowledgments

- Based on concepts from dcc6fvo/unifi-govbr
- Inspired by woodjme/unifi-hotspot
- Built with Django and social-auth-app-django

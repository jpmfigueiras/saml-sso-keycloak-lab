# Frontend GID - SSO Login Instructions

## Project Structure

```
src/
├── pages/           # Application pages
│   ├── Login.js     # SSO login page
│   └── Dashboard.js # Main dashboard
├── components/      # Reusable components
│   └── ProtectedRoute.js  # Protected route wrapper
├── context/         # Context API
│   └── AuthContext.js     # Authentication management
├── services/        # API services
│   └── api.js       # Axios configuration and endpoints
└── App.js          # Route configuration
```

## SSO Login System

### How It Works

1. **Login Page** (`/login`)
   - User enters corporate email
   - Clicks "Continue with SSO"
   - Redirected to configured SSO provider

2. **Authentication**
   - SSO provider validates credentials
   - Returns user data
   - System stores data in localStorage
   - Redirects to `/dashboard`

3. **Protected Routes**
   - All routes (except `/login`) are protected
   - Unauthenticated users redirected to `/login`
   - Authentication state persisted in localStorage

### To Implement Real SSO

In `src/pages/Login.js`, in `handleSSOLogin`, replace simulated code with:

```javascript
const handleSSOLogin = async (e) => {
  e.preventDefault();
  setLoading(true);

  // Redirect to your SSO provider (e.g., Azure AD, Okta, Auth0)
  const redirectUri = `${window.location.origin}/callback`;
  const ssoUrl = `https://your-sso-provider.com/authorize?` +
    `email=${encodeURIComponent(email)}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}`;
  
  window.location.href = ssoUrl;
};
```

### Create Callback Page

Create `src/pages/Callback.js`:

```javascript
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Callback() {
  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    // Process SSO token/data
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    
    if (token) {
      // Validate token with backend
      // Get user data
      login(userData);
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  }, []);

  return <div>Processing login...</div>;
}
```

## Customization

### Colors and Branding

Edit gradients in `src/pages/Login.css`:

```css
.login-container {
  background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
}
```

### Company Logo

Add image to Login component:

```jsx
<div className="login-header">
  <img src="/logo.png" alt="Logo" style={{width: '120px', marginBottom: '16px'}} />
  <h1>GID</h1>
  <p>Integrated Management System</p>
</div>
```

## Test Locally

```bash
# Install dependencies
npm install

# Start development server
npm start
```

Access: http://localhost:3000

## Important Notes

- Current login is **simulated** for demonstration
- In production, implement real SSO with trusted provider
- Data stored in `localStorage` (consider `httpOnly cookies` for production)
- Configure CORS in backend to accept frontend requests

## Popular SSO Providers

- **Azure AD**: For Microsoft enterprises
- **Okta**: Complete enterprise solution
- **Auth0**: Easy integration
- **Google Workspace**: For Google enterprises
- **Keycloak**: Open source, self-hosted

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Login.css';

function Login() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleSSOLogin = (e) => {
    e.preventDefault();
    window.location.href = 'http://localhost:8000/auth/login';
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>GID</h1>
          <p>Integrated Management System</p>
        </div>

        <form onSubmit={handleSSOLogin} className="login-form">
          <button 
            type="submit" 
            className="sso-button"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8zm-1-13v6l5.25 3.15.75-1.23-4.5-2.67V5h-1.5z" fill="currentColor"/>
            </svg>
            Continue with SSO
          </button>
        </form>

        <div className="login-footer">
          <p className="security-note">
            Secure login via Single Sign-On
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;

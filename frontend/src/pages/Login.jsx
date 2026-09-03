import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { loginUser } from '../services/authService';
import './Login.css';
import vetriLogo from '../assets/vetri_logo.jpg';

function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    async function handleLogin(event) {
        event.preventDefault();

        setError('');
        setLoading(true);

        try {
            const data = await loginUser(username, password);

            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            navigate('/dashboard');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-page">

            <div className="login-card">

                {/* Logo */}
                <div className="text-center">
                    <img
                        src={vetriLogo}
                        alt="Vetri IT Systems"
                        className="login-logo"
                    />

                    <h2 className="login-title">
                        Vetri AI Multi Agent
                    </h2>

                    <p className="login-subtitle">
                        AI-Powered Business Operations Platform
                    </p>
                </div>

                <div className="login-divider"></div>

                <h5 className="login-heading">
                    <i className="bi bi-box-arrow-in-right me-2"></i>
                    Login
                </h5>

                {error && (
                    <div className="alert alert-danger login-alert">
                        <i className="bi bi-exclamation-triangle-fill me-2"></i>
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin}>

                    {/* Username */}
                    <div className="mb-3">

                        <label className="form-label">
                            Username
                        </label>

                        <div className="input-group">

                            <span className="input-group-text">
                                <i className="bi bi-person-fill"></i>
                            </span>

                            <input
                                type="text"
                                className="form-control"
                                value={username}
                                onChange={(event) =>
                                    setUsername(event.target.value)
                                }
                                placeholder="Enter username"
                                required
                            />

                        </div>

                    </div>

                    {/* Password */}
                    <div className="mb-4">

                        <label className="form-label">
                            Password
                        </label>

                        <div className="input-group">

                            <span className="input-group-text">
                                <i className="bi bi-lock-fill"></i>
                            </span>

                            <input
                                type={showPassword ? 'text' : 'password'}
                                className="form-control"
                                value={password}
                                onChange={(event) =>
                                    setPassword(event.target.value)
                                }
                                placeholder="Enter password"
                                required
                            />

                            <button
                                type="button"
                                className="btn btn-outline-secondary"
                                onClick={() =>
                                    setShowPassword(!showPassword)
                                }
                            >
                                <i
                                    className={
                                        showPassword
                                            ? 'bi bi-eye-slash-fill'
                                            : 'bi bi-eye-fill'
                                    }
                                ></i>
                            </button>

                        </div>

                    </div>

                    {/* Login Button */}
                    <button
                        type="submit"
                        className="btn login-button w-100"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <span
                                    className="spinner-border spinner-border-sm me-2"
                                    role="status"
                                    aria-hidden="true"
                                ></span>

                                Logging in...
                            </>
                        ) : (
                            <>
                                <i className="bi bi-box-arrow-in-right me-2"></i>
                                Login
                            </>
                        )}
                    </button>

                </form>

                <div className="login-footer">
                    <i className="bi bi-shield-check me-1"></i>
                    Secure AI Business Platform
                </div>

            </div>

        </div>
    );
}

export default Login;
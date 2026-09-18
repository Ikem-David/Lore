import { useState } from 'react';
import './login.css';
import { useNavigate } from 'react-router-dom';

const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$/;
const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

const Login = () => {
    const navigate = useNavigate()
    const [isSignUp, setIsSignUp] = useState(false);
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [signUpData, setSignUpData] = useState({ username: '', email: '', password: '' });
    const [errors, setErrors] = useState({ email: '', password: '' });
    const [signUpErrors, setSignUpErrors] = useState({ username: '', email: '', password: '' });
    const [submitError, setSubmitError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const validateField = (name, value) => {
        if (!value.trim()) {
            const labels = { username: 'Username', email: 'Email', password: 'Password' };
            return `${labels[name]} is required.`;
        }

        if (name === 'email' && !emailRegex.test(value)) {
            return 'Please enter a valid email address.';
        }

        if (name === 'username' && !usernameRegex.test(value)) {
            return 'Username must be 3-20 characters and contain only letters, numbers, or underscores.';
        }

        if (name === 'password' && !passwordRegex.test(value)) {
            return 'Password must be at least 8 characters and include uppercase, lowercase, a number, and a special character.';
        }

        return '';
    };

    const showSignUp = () => {
        setIsSignUp(true);
        setSubmitError('');
        setSuccessMessage('');
    };

    const showLogin = () => {
        setIsSignUp(false);
        setSubmitError('');
        setSuccessMessage('');
    };

    const handleChange = (event) => {
        const { name, value } = event.target;

        setFormData((prev) => ({ ...prev, [name]: value }));
        setErrors((prev) => ({
            ...prev,
            [name]: validateField(name, value),
        }));

        if (submitError) {
            setSubmitError('');
        }
    };

    const handleSignUpChange = (event) => {
        const { name, value } = event.target;

        setSignUpData((prev) => ({ ...prev, [name]: value }));
        setSignUpErrors((prev) => ({
            ...prev,
            [name]: validateField(name, value),
        }));
    };

    const handleSignUpSubmit = async (event) => {
        event.preventDefault();

        const nextErrors = {
            username: validateField('username', signUpData.username),
            email: validateField('email', signUpData.email),
            password: validateField('password', signUpData.password),
        };

        setSignUpErrors(nextErrors);

        if (nextErrors.username || nextErrors.email || nextErrors.password) {
            setSubmitError('');
            return;
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/users/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(signUpData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Invalid email or password. Please try again.');
            }

            setSubmitError('');
            setSuccessMessage('Account created successfully. Please log in.');
            setTimeout(() => setIsSignUp(false), 1500);
        } catch (error) {
            setSuccessMessage('');
            setSubmitError(error.message || 'Unable to log in. Please try again.');
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const nextErrors = {
            email: validateField('email', formData.email),
            password: validateField('password', formData.password),
        };

        setErrors(nextErrors);

        if (nextErrors.email || nextErrors.password) {
            setSubmitError('');
            return;
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/login/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Invalid email or password. Please try again.');
            }

            localStorage.setItem('token', data.access_token);
            window.dispatchEvent(new Event('auth-change'));
            setSubmitError('');
            setSuccessMessage('Login successful. Redirecting...');
            setTimeout(() => navigate('/home'), 1500);
        } catch (error) {
            setSuccessMessage('');
            setSubmitError(error.message || 'Unable to log in. Please try again.');
        }
    };

    return (
        <div className="login-page">
            <div className="login-card">
                {isSignUp ? (
                    <form className="login-form" onSubmit={handleSignUpSubmit} noValidate>
                        <h1 className="login-title">Create an account</h1>
                        <p className="login-subtitle">Join Lore today</p>

                        <div className="login-field">
                            <label className="login-label" htmlFor="username">Username*</label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                placeholder="Username"
                                className={`login-input ${signUpErrors.username ? 'login-input-error' : ''}`}
                                value={signUpData.username}
                                onChange={handleSignUpChange}
                                aria-invalid={Boolean(signUpErrors.username)}
                            />
                            {signUpErrors.username && <span className="login-error">{signUpErrors.username}</span>}
                        </div>

                        <div className="login-field">
                            <label className="login-label" htmlFor="signUpEmail">Email*</label>
                            <input
                                id="signUpEmail"
                                name="email"
                                type="email"
                                placeholder="example@gmail.com"
                                className={`login-input ${signUpErrors.email ? 'login-input-error' : ''}`}
                                value={signUpData.email}
                                onChange={handleSignUpChange}
                                aria-invalid={Boolean(signUpErrors.email)}
                            />
                            {signUpErrors.email && <span className="login-error">{signUpErrors.email}</span>}
                        </div>

                        <div className="login-field">
                            <label className="login-label" htmlFor="signUpPassword">Password*</label>
                            <input
                                id="signUpPassword"
                                name="password"
                                type="password"
                                placeholder="Password"
                                className={`login-input ${signUpErrors.password ? 'login-input-error' : ''}`}
                                value={signUpData.password}
                                onChange={handleSignUpChange}
                                aria-invalid={Boolean(signUpErrors.password)}
                            />
                            {signUpErrors.password && <span className="login-error">{signUpErrors.password}</span>}
                        </div>

                        {submitError && <div className="login-api-error">{submitError}</div>}
                        {successMessage && <div className="login-success">{successMessage}</div>}

                        <button type="submit" className="login-button">Sign Up</button>
                        <p className="login-switch">Already have an account? <button type="button" className="login-link" onClick={showLogin}>Log in</button></p>
                    </form>
                ) : (
                    <form className="login-form" onSubmit={handleSubmit} noValidate>
                        <h1 className="login-title">Lore</h1>
                        <p className="login-subtitle">Welcome back to Lore</p>

                        <div className="login-field">
                            <label className="login-label" htmlFor="email">Email*</label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                placeholder="example@gmail.com"
                                className={`login-input ${errors.email ? 'login-input-error' : ''}`}
                                value={formData.email}
                                onChange={handleChange}
                                aria-invalid={Boolean(errors.email)}
                            />
                            {errors.email && <span className="login-error">{errors.email}</span>}
                        </div>

                        <div className="login-field">
                            <label className="login-label" htmlFor="password">Password*</label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                placeholder="Password"
                                className={`login-input ${errors.password ? 'login-input-error' : ''}`}
                                value={formData.password}
                                onChange={handleChange}
                                aria-invalid={Boolean(errors.password)}
                            />
                            {errors.password && <span className="login-error">{errors.password}</span>}
                        </div>

                        {submitError && <div className="login-api-error">{submitError}</div>}
                        {successMessage && <div className="login-success">{successMessage}</div>}

                        <button type="submit" className="login-button">Log In</button>
                        <p className="login-switch">Don't have an account? <button type="button" className="login-link" onClick={showSignUp}>Sign up</button></p>
                    </form>
                )}
            </div>
        </div>
    );
};

export default Login;
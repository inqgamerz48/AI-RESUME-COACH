/**
 * Register Page
 */
import { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import anime from 'animejs/lib/anime.es.js';
import { authService } from '../services/api';
import { useAuthStore } from '../store/store';
import Button from '../components/Button';

export default function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const setAuth = useAuthStore((state) => state.setAuth);
    const navigate = useNavigate();
    const containerRef = useRef(null);

    useEffect(() => {
        // Stagger animation for form elements
        anime({
            targets: containerRef.current.querySelectorAll('.register-anim'),
            translateY: [20, 0],
            opacity: [0, 1],
            delay: anime.stagger(100),
            easing: 'easeOutExpo',
            duration: 800
        });
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (password.length < 8) {
            setError('Password must be at least 8 characters long');
            return;
        }

        setLoading(true);

        try {
            const data = await authService.register(email, password, fullName);
            setAuth(data.user, data.access_token);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center px-4 py-12" ref={containerRef}>
            <div className="max-w-md w-full">
                <div className="text-center mb-8 register-anim opacity-0">
                    <h1 className="text-4xl font-bold gradient-text mb-2">Get Started</h1>
                    <p className="text-gray-600">Create your account to start building resumes</p>
                </div>

                <div className="card register-anim opacity-0">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {error && (
                            <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded register-anim">
                                {error}
                            </div>
                        )}

                        <div className="register-anim opacity-0">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Full Name
                            </label>
                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                className="input-field"
                                placeholder="John Doe"
                            />
                        </div>

                        <div className="register-anim opacity-0">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Email Address
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="input-field"
                                placeholder="you@example.com"
                                required
                            />
                        </div>

                        <div className="register-anim opacity-0">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Password (min. 8 characters)
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="input-field"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <div className="register-anim opacity-0">
                            <Button type="submit" disabled={loading} className="w-full">
                                {loading ? 'Creating account...' : 'Create Account'}
                            </Button>
                        </div>
                    </form>

                    <div className="mt-6 text-center register-anim opacity-0">
                        <p className="text-gray-600">
                            Already have an account?{' '}
                            <Link to="/login" className="text-primary-600 font-semibold hover:underline">
                                Sign in
                            </Link>
                        </p>
                    </div>
                </div>

                <div className="mt-6 p-4 bg-primary-50 rounded-lg border border-primary-200 register-anim opacity-0">
                    <p className="text-sm text-primary-800 text-center">
                        🎉 <strong>FREE plan</strong> includes 3 AI improvements and 1 resume
                    </p>
                </div>
            </div>
        </div>
    );
}

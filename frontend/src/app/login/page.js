'use client';

/**
 * Login Page
 */
import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import anime from 'animejs';
import { authService } from '@/services/api';
import { useAuthStore } from '@/store/store';
import Button from '@/components/Button';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const setAuth = useAuthStore((state) => state.setAuth);
    const router = useRouter();
    const containerRef = useRef(null);

    useEffect(() => {
        // Stagger animation for form elements
        anime({
            targets: containerRef.current.querySelectorAll('.login-anim'),
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
        setLoading(true);

        try {
            const data = await authService.login(email, password);
            setAuth(data.user, data.access_token);
            router.push('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center px-4 py-12" ref={containerRef}>
            <div className="max-w-md w-full">
                <div className="text-center mb-8 login-anim opacity-0">
                    <h1 className="text-4xl font-bold gradient-text mb-2">Welcome Back</h1>
                    <p className="text-gray-600">Sign in to continue building your resume</p>
                </div>

                <div className="card login-anim opacity-0">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {error && (
                            <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded login-anim">
                                {error}
                            </div>
                        )}

                        <div className="login-anim opacity-0">
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

                        <div className="login-anim opacity-0">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                                Password
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

                        <div className="login-anim opacity-0">
                            <Button type="submit" disabled={loading} className="w-full">
                                {loading ? 'Signing in...' : 'Sign In'}
                            </Button>
                        </div>
                    </form>

                    <div className="mt-6 text-center login-anim opacity-0">
                        <p className="text-gray-600">
                            Don't have an account?{' '}
                            <Link href="/register" className="text-primary-600 font-semibold hover:underline">
                                Sign up
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

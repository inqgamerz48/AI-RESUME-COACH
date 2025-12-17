'use client';

/**
 * Navigation Header
 */
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import anime from 'animejs';
import { useAuthStore } from '@/store/store';

export default function Navbar() {
    // Prevent hydration mismatch by waiting for client load
    const [mounted, setMounted] = useState(false);
    const { user, isAuthenticated, logout } = useAuthStore();
    const router = useRouter();

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleLogout = () => {
        logout();
        router.push('/login');
    };

    const navRef = useRef(null);

    useEffect(() => {
        if (!mounted) return;

        // Logo Animation
        anime({
            targets: navRef.current.querySelector('.nav-logo'),
            translateX: [-20, 0],
            opacity: [0, 1],
            easing: 'easeOutExpo',
            duration: 800,
            delay: 200
        });

        // Links Animation
        anime({
            targets: navRef.current.querySelectorAll('.nav-link'),
            translateY: [-20, 0],
            opacity: [0, 1],
            easing: 'easeOutExpo',
            duration: 800,
            delay: anime.stagger(100, { start: 400 })
        });
    }, [mounted]);

    // Don't render until mounted to avoid hydration errors with store state
    if (!mounted) {
        return (
            <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-40 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        {/* Static Logo Placeholder */}
                        <div className="flex items-center space-x-2">
                            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-accent-600 rounded-lg flex items-center justify-center">
                                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <span className="text-xl font-bold gradient-text">AI Resume Coach</span>
                        </div>
                    </div>
                </div>
            </nav>
        );
    }

    return (
        <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-40 shadow-sm" ref={navRef}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2 nav-logo opacity-0">
                        <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-accent-600 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <span className="text-xl font-bold gradient-text">AI Resume Coach</span>
                    </Link>

                    {/* Navigation */}
                    <div className="flex items-center space-x-6">
                        {isAuthenticated ? (
                            <>
                                <Link href="/dashboard" className="text-gray-700 hover:text-primary-600 font-medium transition nav-link opacity-0">
                                    Dashboard
                                </Link>
                                <Link href="/resume-analyzer" className="text-gray-700 hover:text-primary-600 font-medium transition nav-link opacity-0">
                                    Analyzer
                                </Link>
                                <Link href="/pricing" className="text-gray-700 hover:text-primary-600 font-medium transition nav-link opacity-0">
                                    Pricing
                                </Link>

                                {/* User Menu */}
                                <div className="flex items-center space-x-4 nav-link opacity-0">
                                    <div className="text-right">
                                        <p className="text-sm font-semibold text-gray-900">{user?.email}</p>
                                        <p className="text-xs font-medium text-accent-600">{user?.plan} Plan</p>
                                    </div>

                                    <button
                                        onClick={handleLogout}
                                        className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition"
                                    >
                                        Logout
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                <Link href="/pricing" className="text-gray-700 hover:text-primary-600 font-medium transition nav-link opacity-0">
                                    Pricing
                                </Link>
                                <Link href="/login" className="text-gray-700 hover:text-primary-600 font-medium transition nav-link opacity-0">
                                    Login
                                </Link>
                                <div className="nav-link opacity-0">
                                    <Link href="/register" className="px-6 py-2 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 active:scale-95 inline-block">
                                        Get Started
                                    </Link>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}

/**
 * Feature Lock Component - Shows upgrade CTA when feature is locked
 */
import { useEffect, useRef } from 'react';
import { useUIStore } from '../store/store';
import anime from 'animejs/lib/anime.es.js';

export default function FeatureLock({ feature, plan, children }) {
    const setShowUpgradeModal = useUIStore((state) => state.setShowUpgradeModal);
    const lockRef = useRef(null);

    useEffect(() => {
        if (lockRef.current) {
            anime({
                targets: lockRef.current.querySelector('.lock-icon'),
                scale: [0.8, 1],
                opacity: [0, 1],
                easing: 'easeOutElastic(1, .8)',
                duration: 1000,
                delay: 200
            });
        }
    }, [plan]);

    const handleClick = () => {
        // Shake animation on click to indicate locked
        if (lockRef.current) {
            anime({
                targets: lockRef.current,
                translateX: [
                    { value: -5, duration: 50 },
                    { value: 5, duration: 50 },
                    { value: -5, duration: 50 },
                    { value: 5, duration: 50 },
                    { value: 0, duration: 50 }
                ],
                easing: 'linear'
            });
        }

        setShowUpgradeModal(
            true,
            `This feature is only available in ${plan} plan. Upgrade to unlock!`
        );
    };

    return (
        <div className="relative group">
            <div className="feature-locked opacity-50 pointer-events-none filter blur-[1px] select-none">
                {children}
            </div>
            <div
                ref={lockRef}
                className="absolute inset-0 flex items-center justify-center bg-white/60 backdrop-blur-[2px] rounded-lg cursor-pointer transition-colors hover:bg-white/70 z-10"
                onClick={handleClick}
            >
                <div className="bg-white/90 px-6 py-4 rounded-xl shadow-lg border border-gray-100 text-center transform transition-transform group-hover:scale-105">
                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full mx-auto mb-3 lock-icon opacity-0 shadow-inner">
                        <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                    </div>
                    <p className="text-sm font-bold text-gray-800 mb-1">
                        Locked Feature
                    </p>
                    <p className="text-xs text-purple-600 font-semibold uppercase tracking-wider mb-3">
                        {plan} Plan
                    </p>
                    <button className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-xs font-bold uppercase tracking-wide rounded-lg shadow-md hover:shadow-lg transition-all">
                        Upgrade
                    </button>
                </div>
            </div>
        </div>
    );
}

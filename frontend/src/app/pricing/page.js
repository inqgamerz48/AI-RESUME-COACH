'use client';

/**
 * Pricing Page - Shows all 3 tiers
 */
import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import anime from 'animejs';
import { billingService } from '@/services/api';
import { useAuthStore, useUIStore } from '@/store/store';
import Button from '@/components/Button';

export default function Pricing() {
    const [plans, setPlans] = useState([]);
    // const [loading, setLoading] = useState(true); // Default false for static/mock data if preferred, but keeping true
    const { user, isAuthenticated } = useAuthStore();
    const setShowUpgradeModal = useUIStore((state) => state.setShowUpgradeModal);
    const router = useRouter();
    const containerRef = useRef(null);

    // Initial loading state
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadPlans();
    }, []);

    const loadPlans = async () => {
        try {
            const data = await billingService.getPlans();
            setPlans(data.plans);
            // Run animation after plans are loaded
            setTimeout(() => {
                if (containerRef.current) {
                    anime({
                        targets: containerRef.current.querySelectorAll('.pricing-anim'),
                        translateY: [20, 0],
                        opacity: [0, 1],
                        delay: anime.stagger(150),
                        easing: 'easeOutExpo',
                        duration: 800
                    });
                }
            }, 100);
        } catch (error) {
            console.error('Failed to load plans:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSelectPlan = (planTier) => {
        if (!isAuthenticated) {
            router.push('/register');
            return;
        }

        if (user?.plan === planTier) {
            alert('You are already on this plan');
            return;
        }

        // TODO: Integrate with payment provider
        // For now, show a placeholder modal
        setShowUpgradeModal(
            true,
            `Payment integration coming soon! This will upgrade you to the ${planTier} plan.`
        );
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading pricing plans...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen py-12 px-4" ref={containerRef}>
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12 pricing-anim opacity-0">
                    <h1 className="text-5xl font-bold gradient-text mb-4">
                        Choose Your Plan
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Start with our FREE plan or upgrade for unlimited AI-powered resume building
                    </p>
                </div>

                {/* Pricing Cards */}
                <div className="grid md:grid-cols-3 gap-8 mb-12">
                    {plans.map((plan, index) => (
                        <div
                            key={plan.tier}
                            className={`${plan.popular ? 'pricing-card-popular' : 'pricing-card'
                                } relative pricing-anim opacity-0`}
                        >
                            {plan.popular && (
                                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                                    <span className="bg-gradient-to-r from-primary-600 to-accent-600 text-white px-4 py-1 rounded-full text-sm font-bold shadow-lg">
                                        MOST POPULAR
                                    </span>
                                </div>
                            )}

                            <div className="mb-6">
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                                    {plan.name}
                                </h3>
                                <div className="flex items-baseline">
                                    <span className="text-5xl font-bold text-gray-900">
                                        ${plan.price}
                                    </span>
                                    {plan.price > 0 && (
                                        <span className="text-gray-500 ml-2">/month</span>
                                    )}
                                </div>
                                {plan.recommended_for && (
                                    <p className="text-sm text-accent-600 mt-2 font-medium">
                                        {plan.recommended_for}
                                    </p>
                                )}
                            </div>

                            <ul className="space-y-3 mb-8">
                                {plan.features.map((feature, idx) => (
                                    <li key={idx} className="flex items-start">
                                        <svg
                                            className="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                strokeWidth={2}
                                                d="M5 13l4 4L19 7"
                                            />
                                        </svg>
                                        <span className="text-gray-700">{feature}</span>
                                    </li>
                                ))}
                            </ul>

                            {plan.limitations && (
                                <ul className="space-y-2 mb-6 pb-6 border-b border-gray-200">
                                    {plan.limitations.map((limitation, idx) => (
                                        <li key={idx} className="flex items-start">
                                            <svg
                                                className="w-5 h-5 text-red-400 mr-2 flex-shrink-0 mt-0.5"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    strokeWidth={2}
                                                    d="M6 18L18 6M6 6l12 12"
                                                />
                                            </svg>
                                            <span className="text-gray-500 text-sm">{limitation}</span>
                                        </li>
                                    ))}
                                </ul>
                            )}

                            <Button
                                onClick={() => handleSelectPlan(plan.tier)}
                                variant={plan.popular ? 'primary' : 'secondary'}
                                className="w-full"
                            >
                                {user?.plan === plan.tier
                                    ? 'Current Plan'
                                    : plan.price === 0
                                        ? 'Get Started Free'
                                        : `Upgrade to ${plan.name}`}
                            </Button>
                        </div>
                    ))}
                </div>

                {/* Payment Integration Notice */}
                <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg pricing-anim opacity-0">
                    <div className="flex">
                        <svg
                            className="w-6 h-6 text-yellow-400 mr-3 flex-shrink-0"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                        <div>
                            <h4 className="font-bold text-yellow-800 mb-1">Payment Integration Notice</h4>
                            <p className="text-yellow-700 text-sm">
                                This is an MVP version. Payment integration with Stripe/Razorpay is ready to be implemented.
                                See README.md for integration instructions.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

/**
 * Feature Lock Component - Shows upgrade CTA when feature is locked
 */
import { useUIStore } from '../store/store';

export default function FeatureLock({ feature, plan, children }) {
    const setShowUpgradeModal = useUIStore((state) => state.setShowUpgradeModal);

    const handleClick = () => {
        setShowUpgradeModal(
            true,
            `This feature is only available in ${plan} plan. Upgrade to unlock!`
        );
    };

    return (
        <div className="relative">
            <div className="feature-locked">{children}</div>
            <div
                className="absolute inset-0 flex items-center justify-center bg-black/30 backdrop-blur-sm rounded-lg cursor-pointer"
                onClick={handleClick}
            >
                <div className="bg-white px-6 py-4 rounded-lg shadow-xl text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-accent-100 rounded-full mx-auto mb-2">
                        <svg className="w-6 h-6 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                    </div>
                    <p className="text-sm font-semibold text-gray-900">
                        {plan} Feature
                    </p>
                    <button className="mt-2 px-4 py-2 bg-accent-600 text-white text-sm font-semibold rounded-lg hover:bg-accent-700 transition">
                        Upgrade Now
                    </button>
                </div>
            </div>
        </div>
    );
}

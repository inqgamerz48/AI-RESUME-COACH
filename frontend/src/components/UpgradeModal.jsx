/**
 * Upgrade Modal Component
 */
import { useUIStore } from '../store/store';
import { useNavigate } from 'react-router-dom';

export default function UpgradeModal() {
    const { showUpgradeModal, upgradeMessage, setShowUpgradeModal } = useUIStore();
    const navigate = useNavigate();

    if (!showUpgradeModal) return null;

    const handleUpgrade = () => {
        setShowUpgradeModal(false);
        navigate('/pricing');
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl max-w-md w-full p-8 shadow-2xl animate-scale-in">
                <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-br from-accent-100 to-primary-100 rounded-full mx-auto mb-4">
                    <svg className="w-8 h-8 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>

                <h2 className="text-2xl font-bold text-center mb-2">Upgrade Required</h2>

                <p className="text-gray-600 text-center mb-6">
                    {upgradeMessage}
                </p>

                <div className="space-y-3">
                    <button
                        onClick={handleUpgrade}
                        className="w-full btn-primary"
                    >
                        View Pricing Plans
                    </button>

                    <button
                        onClick={() => setShowUpgradeModal(false)}
                        className="w-full px-6 py-3 text-gray-600 font-semibold hover:bg-gray-100 rounded-lg transition"
                    >
                        Maybe Later
                    </button>
                </div>
            </div>
        </div>
    );
}

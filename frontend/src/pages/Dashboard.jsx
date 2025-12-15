/**
 * Dashboard - Resume Builder with AI Chat
 */
import { useState } from 'react';
import { useAuthStore, useUIStore } from '../store/store';
import { aiService } from '../services/api';
import Button from '../components/Button';
import FeatureLock from '../components/FeatureLock';

export default function Dashboard() {
    const { user } = useAuthStore();
    const setShowUpgradeModal = useUIStore((state) => state.setShowUpgradeModal);

    const [inputText, setInputText] = useState('');
    const [aiResponse, setAiResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [usage, setUsage] = useState(null);
    const [error, setError] = useState('');

    const handleRewrite = async () => {
        if (!inputText.trim()) {
            setError('Please enter some text to rewrite');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const data = await aiService.rewriteBullet(inputText, 'professional');
            setAiResponse(data.result);
            setUsage(data.usage);
        } catch (err) {
            const errorData = err.response?.data?.detail;
            if (errorData?.upgrade_required) {
                setShowUpgradeModal(true, errorData.message);
            } else {
                setError(errorData?.message || 'Failed to process request');
            }
        } finally {
            setLoading(false);
        }
    };

    const canUseProFeatures = user?.plan === 'PRO' || user?.plan === 'ULTIMATE';
    const canUseUltimateFeatures = user?.plan === 'ULTIMATE';

    return (
        <div className="min-h-screen py-12 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold gradient-text mb-2">
                        Resume Builder Dashboard
                    </h1>
                    <p className="text-gray-600">
                        Welcome back! You're on the <strong>{user?.plan}</strong> plan
                    </p>

                    {/* Usage Stats */}
                    {usage && (
                        <div className="mt-4 inline-flex items-center space-x-2 bg-primary-50 px-4 py-2 rounded-lg">
                            <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            <span className="text-sm font-semibold text-primary-900">
                                AI Usage: {usage.used}/{usage.limit} ({usage.remaining} remaining)
                            </span>
                        </div>
                    )}

                    {/* Resume Analyzer CTA */}
                    <div className="mt-6 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
                        <div className="flex items-center justify-between">
                            <div className="flex-1">
                                <h3 className="text-xl font-bold mb-2 flex items-center">
                                    <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    New: AI Resume Analyzer
                                </h3>
                                <p className="text-indigo-100 text-sm">
                                    Upload your resume, get AI-powered analysis, and download an enhanced version
                                </p>
                            </div>
                            <a
                                href="/resume-analyzer"
                                className="ml-4 bg-white text-indigo-600 font-bold py-3 px-6 rounded-lg hover:bg-indigo-50 transition-all transform hover:scale-105 shadow-lg whitespace-nowrap"
                            >
                                Try Now →
                            </a>
                        </div>
                    </div>
                </div>

                <div className="grid lg:grid-cols-2 gap-8">
                    {/* Left: AI Chat */}
                    <div className="space-y-6">
                        {/* Basic Rewrite - ALL TIERS */}
                        <div className="card">
                            <h2 className="text-2xl font-bold mb-4">
                                ✨ AI Resume Improver
                            </h2>

                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Enter your resume bullet point
                                    </label>
                                    <textarea
                                        value={inputText}
                                        onChange={(e) => setInputText(e.target.value)}
                                        className="input-field min-h-[120px]"
                                        placeholder="e.g. Worked on a website project using React"
                                        maxLength={300}
                                    />
                                    <p className="text-xs text-gray-500 mt-1">
                                        {inputText.length}/300 characters
                                    </p>
                                </div>

                                {error && (
                                    <div className="p-3 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm rounded">
                                        {error}
                                    </div>
                                )}

                                <Button onClick={handleRewrite} disabled={loading} className="w-full">
                                    {loading ? 'Improving...' : 'Improve with AI'}
                                </Button>

                                {aiResponse && (
                                    <div className="p-4 bg-green-50 border-2 border-green-200 rounded-lg">
                                        <h4 className="font-semibold text-green-900 mb-2">✅ Improved Version:</h4>
                                        <p className="text-green-800">{aiResponse}</p>
                                        <button
                                            onClick={() => navigator.clipboard.writeText(aiResponse)}
                                            className="mt-2 text-sm text-green-600 hover:text-green-800 font-medium"
                                        >
                                            📋 Copy to clipboard
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Project Generation - PRO & ULTIMATE */}
                        {canUseProFeatures ? (
                            <div className="card">
                                <h2 className="text-2xl font-bold mb-4">
                                    🚀 Project Description Generator
                                </h2>
                                <p className="text-gray-600 text-sm">
                                    Generate professional project descriptions for your resume
                                </p>
                                {/* Add project generation form here */}
                            </div>
                        ) : (
                            <FeatureLock feature="project_gen" plan="PRO">
                                <div className="card">
                                    <h2 className="text-2xl font-bold mb-4">
                                        🚀 Project Description Generator
                                    </h2>
                                    <input className="input-field mb-3" placeholder="Project Name" disabled />
                                    <input className="input-field mb-3" placeholder="Tech Stack" disabled />
                                    <textarea className="input-field min-h-[100px]" placeholder="Key Points" disabled />
                                </div>
                            </FeatureLock>
                        )}

                        {/* Summary Generation - PRO & ULTIMATE */}
                        {canUseProFeatures ? (
                            <div className="card">
                                <h2 className="text-2xl font-bold mb-4">
                                    📝 Resume Summary Generator
                                </h2>
                                <p className="text-gray-600 text-sm">
                                    Create a powerful resume summary statement
                                </p>
                                {/* Add summary generation form here */}
                            </div>
                        ) : (
                            <FeatureLock feature="summary" plan="PRO">
                                <div className="card">
                                    <h2 className="text-2xl font-bold mb-4">
                                        📝 Resume Summary Generator
                                    </h2>
                                    <input className="input-field mb-3" placeholder="Your Skills" disabled />
                                    <input className="input-field mb-3" placeholder="Experience" disabled />
                                    <input className="input-field" placeholder="Career Goal" disabled />
                                </div>
                            </FeatureLock>
                        )}
                    </div>

                    {/* Right: Resume Preview */}
                    <div className="space-y-6">
                        <div className="card sticky top-24">
                            <h2 className="text-2xl font-bold mb-4">📄 Resume Preview</h2>

                            <div className="bg-gray-50 rounded-lg p-6 min-h-[600px] border-2 border-dashed border-gray-300">
                                <div className="text-center text-gray-500 mt-20">
                                    <svg className="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    <p className="font-semibold text-lg">Your resume preview will appear here</p>
                                    <p className="text-sm mt-2">Start adding content using the AI tools</p>
                                </div>
                            </div>

                            <div className="mt-4 flex space-x-3">
                                <Button variant="secondary" className="flex-1">
                                    Save Resume
                                </Button>
                                <Button variant="primary" className="flex-1">
                                    Export PDF
                                </Button>
                            </div>

                            {user?.plan === 'FREE' && (
                                <p className="text-xs text-gray-500 text-center mt-2">
                                    ⚠️ FREE plan PDFs include a watermark
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

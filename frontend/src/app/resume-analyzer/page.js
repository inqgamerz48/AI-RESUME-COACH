'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, FileSearch } from 'lucide-react';
import anime from 'animejs';
import ResumeUploader from '@/components/ResumeUploader';
import AnalysisResults from '@/components/AnalysisResults';
import EnhancementSummary from '@/components/EnhancementSummary';

const ResumeAnalyzerPage = () => {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState(1); // 1: Upload, 2: Analysis, 3: Enhancement
    const [isLoading, setIsLoading] = useState(false);
    const [analysisData, setAnalysisData] = useState(null);
    const [enhancementData, setEnhancementData] = useState(null);

    const containerRef = useRef(null);

    useEffect(() => {
        // Initial entry animation
        const timeline = anime.timeline({
            easing: 'easeOutExpo',
            duration: 800
        });

        timeline
            .add({
                targets: containerRef.current.querySelector('.analyzer-header'),
                translateY: [-20, 0],
                opacity: [0, 1],
                duration: 600
            })
            .add({
                targets: containerRef.current.querySelector('.analyzer-steps'),
                translateY: [20, 0],
                opacity: [0, 1],
                duration: 600
            }, '-=300')
            .add({
                targets: containerRef.current.querySelectorAll('.analyzer-anim-item'),
                translateY: [20, 0],
                opacity: [0, 1],
                delay: anime.stagger(100),
                duration: 600
            }, '-=300');
    }, []);

    // Animate content change
    useEffect(() => {
        if (containerRef.current) {
            anime({
                targets: containerRef.current.querySelector('.analyzer-content'),
                opacity: [0, 1],
                translateY: [10, 0],
                easing: 'easeOutQuad',
                duration: 400
            });
        }
    }, [currentStep]);

    const handleUploadSuccess = (data) => {
        setAnalysisData(data);
        setCurrentStep(2);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleProceedToEnhance = async (selectedSuggestions) => {
        if (selectedSuggestions.length === 0) {
            alert('Please select at least one suggestion to apply');
            return;
        }

        setIsLoading(true);

        try {
            const token = localStorage.getItem('access_token');
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(
                `${apiUrl}/api/v1/resume/enhance/${analysisData.analysis_id}`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(selectedSuggestions),
                }
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Enhancement failed');
            }

            const data = await response.json();
            setEnhancementData(data);
            setCurrentStep(3);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } catch (error) {
            console.error('Enhancement error:', error);
            alert(error.message || 'Error enhancing resume. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleStartNew = () => {
        setCurrentStep(1);
        setAnalysisData(null);
        setEnhancementData(null);
        setIsLoading(false);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const steps = [
        { number: 1, name: 'Upload Resume', active: currentStep === 1, completed: currentStep > 1 },
        { number: 2, name: 'View Analysis', active: currentStep === 2, completed: currentStep > 2 },
        { number: 3, name: 'Get Enhanced Resume', active: currentStep === 3, completed: false },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-indigo-50 py-12 px-4" ref={containerRef}>
            {/* Header */}
            <div className="max-w-6xl mx-auto mb-8 analyzer-header opacity-0">
                <button
                    onClick={() => router.push('/dashboard')}
                    className="flex items-center space-x-2 text-gray-600 hover:text-indigo-600 transition-colors mb-6"
                >
                    <ArrowLeft className="w-5 h-5" />
                    <span>Back to Dashboard</span>
                </button>

                <div className="flex items-center space-x-4 mb-6">
                    <div className="p-3 bg-indigo-100 rounded-xl">
                        <FileSearch className="w-8 h-8 text-indigo-600" />
                    </div>
                    <div>
                        <h1 className="text-4xl font-bold text-gray-900">
                            AI Resume Analyzer
                        </h1>
                        <p className="text-gray-600 mt-1">
                            Upload your resume, get AI-powered insights, and download an enhanced version
                        </p>
                    </div>
                </div>

                {/* Progress Steps */}
                <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 analyzer-steps opacity-0">
                    <div className="flex items-center justify-between">
                        {steps.map((step, index) => (
                            <div key={step.number} className="flex items-center flex-1">
                                <div className="flex items-center">
                                    {/* Step Circle */}
                                    <div
                                        className={`flex items-center justify-center w-10 h-10 rounded-full font-bold transition-all ${step.completed
                                            ? 'bg-green-500 text-white'
                                            : step.active
                                                ? 'bg-indigo-600 text-white'
                                                : 'bg-gray-200 text-gray-500'
                                            }`}
                                    >
                                        {step.completed ? '✓' : step.number}
                                    </div>

                                    {/* Step Label */}
                                    <div className="ml-3">
                                        <div
                                            className={`font-semibold ${step.active ? 'text-indigo-600' : step.completed ? 'text-green-600' : 'text-gray-500'
                                                }`}
                                        >
                                            {step.name}
                                        </div>
                                    </div>
                                </div>

                                {/* Connector Line */}
                                {index < steps.length - 1 && (
                                    <div className="flex-1 mx-4">
                                        <div
                                            className={`h-1 rounded-full transition-all ${step.completed ? 'bg-green-500' : 'bg-gray-200'
                                                }`}
                                        ></div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="max-w-6xl mx-auto analyzer-content">
                {currentStep === 1 && (
                    <div className="animate-fadeIn analyzer-anim-item opacity-0">
                        <ResumeUploader
                            onUploadSuccess={handleUploadSuccess}
                            isLoading={isLoading}
                            setIsLoading={setIsLoading}
                        />
                    </div>
                )}

                {currentStep === 2 && analysisData && (
                    <div className="animate-fadeIn analyzer-anim-item opacity-0">
                        <AnalysisResults
                            analysisData={analysisData}
                            onProceedToEnhance={handleProceedToEnhance}
                        />
                    </div>
                )}

                {currentStep === 3 && (
                    <div className="animate-fadeIn analyzer-anim-item opacity-0">
                        <EnhancementSummary
                            enhancementData={enhancementData}
                            isGenerating={isLoading}
                        />

                        {!isLoading && (
                            <div className="mt-6 text-center">
                                <button
                                    onClick={handleStartNew}
                                    className="px-6 py-3 bg-white border-2 border-indigo-600 text-indigo-600 font-semibold rounded-xl hover:bg-indigo-50 transition-all duration-200"
                                >
                                    Analyze Another Resume
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Help Section */}
            <div className="max-w-6xl mx-auto mt-12 analyzer-anim-item opacity-0">
                <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">How It Works</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div>
                            <div className="flex items-center space-x-2 mb-2">
                                <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">
                                    1
                                </div>
                                <h4 className="font-semibold text-gray-900">Upload</h4>
                            </div>
                            <p className="text-sm text-gray-600">
                                Upload your current resume in PDF format (max 5MB)
                            </p>
                        </div>
                        <div>
                            <div className="flex items-center space-x-2 mb-2">
                                <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">
                                    2
                                </div>
                                <h4 className="font-semibold text-gray-900">Analyze</h4>
                            </div>
                            <p className="text-sm text-gray-600">
                                Our AI analyzes content, ATS compatibility, structure, and more
                            </p>
                        </div>
                        <div>
                            <div className="flex items-center space-x-2 mb-2">
                                <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">
                                    3
                                </div>
                                <h4 className="font-semibold text-gray-900">Enhance</h4>
                            </div>
                            <p className="text-sm text-gray-600">
                                Select suggestions and download your AI-enhanced resume
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResumeAnalyzerPage;

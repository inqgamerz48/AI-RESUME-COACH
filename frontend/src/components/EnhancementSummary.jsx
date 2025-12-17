import { useRef, useEffect } from 'react';
import { CheckCircle, Download, TrendingUp, FileText, Sparkles } from 'lucide-react';
import anime from 'animejs';

const EnhancementSummary = ({ enhancementData, isGenerating }) => {
    const containerRef = useRef(null);
    const loadingRef = useRef(null);

    // Animate success state
    useEffect(() => {
        if (!isGenerating && enhancementData && containerRef.current) {
            anime({
                targets: containerRef.current.querySelectorAll('.success-anim'),
                translateY: [20, 0],
                opacity: [0, 1],
                delay: anime.stagger(100),
                easing: 'easeOutExpo',
                duration: 800
            });
        }
    }, [isGenerating, enhancementData]);

    const {
        enhanced_resume_id,
        analysis_id,
        accepted_changes,
        total_suggestions,
        message,
        download_url
    } = enhancementData || {};

    const handleDownload = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000${download_url}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Download failed');
            }

            // Create blob from response
            const blob = await response.blob();

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `enhanced_resume_${enhanced_resume_id}.pdf`;

            document.body.appendChild(a);
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Download error:', error);
            alert('Error downloading resume. Please try again.');
        }
    };

    if (isGenerating) {
        return (
            <div className="w-full max-w-2xl mx-auto">
                <div className="bg-white rounded-2xl shadow-xl p-12 border border-gray-100" ref={loadingRef}>
                    <div className="text-center">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-indigo-100 mb-6">
                            <Sparkles className="w-10 h-10 text-indigo-600 animate-pulse" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">
                            Generating Enhanced Resume...
                        </h2>
                        <p className="text-gray-600 mb-8">
                            Our AI is applying your selected enhancements to create an improved version of your resume.
                        </p>

                        {/* Loading animation */}
                        <div className="flex justify-center space-x-2">
                            <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                            <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                            <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="w-full max-w-3xl mx-auto" ref={containerRef}>
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl shadow-2xl p-8 border-2 border-green-200 success-anim opacity-0">
                {/* Success Header */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-100 mb-4">
                        <CheckCircle className="w-12 h-12 text-green-600" />
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">
                        Resume Enhanced Successfully!
                    </h2>
                    <p className="text-gray-700">
                        {message || 'Your AI-enhanced resume is ready for download'}
                    </p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                    <div className="bg-white rounded-xl p-6 shadow-md border border-green-100">
                        <div className="flex items-center space-x-3">
                            <TrendingUp className="w-8 h-8 text-green-600" />
                            <div>
                                <div className="text-2xl font-bold text-gray-900">{accepted_changes}</div>
                                <div className="text-sm text-gray-600">Enhancements Applied</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl p-6 shadow-md border border-green-100">
                        <div className="flex items-center space-x-3">
                            <FileText className="w-8 h-8 text-indigo-600" />
                            <div>
                                <div className="text-2xl font-bold text-gray-900">{total_suggestions}</div>
                                <div className="text-sm text-gray-600">Total Suggestions</div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl p-6 shadow-md border border-green-100">
                        <div className="flex items-center space-x-3">
                            <Sparkles className="w-8 h-8 text-yellow-600" />
                            <div>
                                <div className="text-2xl font-bold text-gray-900">
                                    {Math.round((accepted_changes / total_suggestions) * 100)}%
                                </div>
                                <div className="text-sm text-gray-600">Improvement Rate</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* What's Improved */}
                <div className="bg-white rounded-xl p-6 shadow-md border border-green-100 mb-8">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">
                        What&apos;s Improved in Your Resume:
                    </h3>
                    <ul className="space-y-3">
                        <li className="flex items-start space-x-3">
                            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700">
                                Professional language and strong action verbs for better impact
                            </span>
                        </li>
                        <li className="flex items-start space-x-3">
                            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700">
                                ATS-optimized formatting for better recruiter visibility
                            </span>
                        </li>
                        <li className="flex items-start space-x-3">
                            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700">
                                Enhanced structure and organization for readability
                            </span>
                        </li>
                        <li className="flex items-start space-x-3">
                            <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700">
                                Fresher-focused content highlighting your potential
                            </span>
                        </li>
                    </ul>
                </div>

                {/* Download Button */}
                <button
                    onClick={handleDownload}
                    className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
                >
                    <span className="flex items-center justify-center space-x-3">
                        <Download className="w-6 h-6" />
                        <span className="text-lg">Download Enhanced Resume (PDF)</span>
                    </span>
                </button>

                {/* Additional Info */}
                <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <p className="text-sm text-blue-800">
                        <strong>Next Steps:</strong> Download your enhanced resume and use it for your job applications.
                        You can also analyze it again to see the improvement or create more variations in your dashboard.
                    </p>
                </div>

                {/* Resume ID Reference */}
                <div className="mt-4 text-center text-xs text-gray-500">
                    Resume ID: #{enhanced_resume_id} • Analysis ID: #{analysis_id}
                </div>
            </div>
        </div>
    );
};

export default EnhancementSummary;

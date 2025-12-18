import { useState, useRef, useEffect } from 'react';
import {
    CheckCircle, XCircle, AlertCircle, TrendingUp, Shield, Layout,
    Briefcase, ChevronDown, ChevronUp, Sparkles
} from 'lucide-react';
import anime from 'animejs';

const AnalysisResults = ({ analysisData, onProceedToEnhance }) => {
    const [selectedSuggestions, setSelectedSuggestions] = useState([]);
    const [expandedCategory, setExpandedCategory] = useState(null);

    const containerRef = useRef(null);

    useEffect(() => {
        // Stagger animation for analysis result blocks
        if (containerRef.current) {
            anime({
                targets: containerRef.current.querySelectorAll('.analysis-anim'),
                translateY: [20, 0],
                opacity: [0, 1],
                delay: anime.stagger(100),
                easing: 'easeOutExpo',
                duration: 800
            });
        }
    }, []);

    // Safety check - ensure analysisData exists
    if (!analysisData) {
        console.error("AnalysisResults: analysisData is null/undefined");
        return <div className="text-center p-8">No analysis data available</div>;
    }

    console.log("AnalysisResults rendering with data:", analysisData);

    const {
        overall_score,
        category_scores,
        suggestions,
        total_suggestions,
        critical_issues,
        metrics,
        tier_info
    } = analysisData;

    // Additional safety check for required fields
    if (!category_scores || !suggestions) {
        console.error("AnalysisResults: Missing required fields", { category_scores, suggestions });
        return <div className="text-center p-8">Invalid analysis data</div>;
    }

    // Group suggestions by category
    const groupedSuggestions = suggestions.reduce((acc, suggestion, index) => {
        const category = suggestion.category;
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push({ ...suggestion, index });
        return acc;
    }, {});

    const handleToggleSuggestion = (index) => {
        setSelectedSuggestions(prev => {
            if (prev.includes(index)) {
                return prev.filter(i => i !== index);
            } else {
                return [...prev, index];
            }
        });
    };

    const getScoreColor = (score) => {
        if (score >= 80) return 'text-green-600';
        if (score >= 60) return 'text-yellow-600';
        return 'text-red-600';
    };

    const getScoreBgColor = (score) => {
        if (score >= 80) return 'bg-green-100';
        if (score >= 60) return 'bg-yellow-100';
        return 'bg-red-100';
    };

    const getSeverityBadge = (severity) => {
        const styles = {
            critical: 'bg-red-100 text-red-800 border-red-200',
            high: 'bg-orange-100 text-orange-800 border-orange-200',
            medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
            low: 'bg-blue-100 text-blue-800 border-blue-200'
        };

        return (
            <span className={`px-2 py-1 rounded-full text-xs font-semibold border ${styles[severity]}`}>
                {severity.toUpperCase()}
            </span>
        );
    };

    const categoryIcons = {
        content_quality: TrendingUp,
        ats_optimization: Shield,
        structure: Layout,
        fresher_specific: Briefcase
    };

    const categoryLabels = {
        content_quality: 'Content Quality',
        ats_optimization: 'ATS Optimization',
        structure: 'Structure & Format',
        fresher_specific: 'Fresher-Specific'
    };

    return (
        <div className="w-full max-w-6xl mx-auto space-y-6" ref={containerRef}>
            {/* Overall Score Card */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-2xl p-8 text-white analysis-anim">
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-3xl font-bold mb-2">Resume Analysis Complete!</h2>
                        <p className="text-indigo-100">
                            Your resume has been analyzed across 4 key categories
                        </p>
                    </div>
                    <div className="text-center">
                        <div className={`text-6xl font-bold ${overall_score >= 70 ? 'text-green-300' : 'text-yellow-300'}`}>
                            {Math.round(overall_score)}
                        </div>
                        <div className="text-sm text-indigo-100 mt-2">Overall Score</div>
                    </div>
                </div>

                {/* Tier Info */}
                {tier_info && (
                    <div className="mt-6 bg-white/10 backdrop-blur-sm rounded-lg p-4">
                        <div className="flex items-center justify-between text-sm">
                            <span>Plan: <strong>{tier_info.current_plan}</strong></span>
                            <span>Analyses Used: <strong>{tier_info.analyses_used}/{tier_info.analyses_limit}</strong></span>
                        </div>
                    </div>
                )}
            </div>

            {/* Category Scores */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 analysis-anim">
                {Object.entries(category_scores).map(([category, score]) => {
                    const Icon = categoryIcons[category];
                    return (
                        <div key={category} className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
                            <div className="flex items-center justify-between mb-4">
                                <Icon className="w-8 h-8 text-indigo-600" />
                                <div className={`text-3xl font-bold ${getScoreColor(score)}`}>
                                    {Math.round(score)}
                                </div>
                            </div>
                            <div className="text-sm font-semibold text-gray-700">
                                {categoryLabels[category]}
                            </div>
                            <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className={`h-2 rounded-full ${score >= 80 ? 'bg-green-500' : score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                                        }`}
                                    style={{ width: `${score}%` }}
                                ></div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Key Metrics */}
            {metrics && (
                <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 analysis-anim">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">Key Metrics</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                            <div className="text-2xl font-bold text-indigo-600">{metrics.word_count}</div>
                            <div className="text-sm text-gray-600 mt-1">Words</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                            <div className="text-2xl font-bold text-indigo-600">{metrics.bullet_points}</div>
                            <div className="text-sm text-gray-600 mt-1">Bullet Points</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                            <div className="text-2xl font-bold text-indigo-600">{metrics.action_verbs}</div>
                            <div className="text-sm text-gray-600 mt-1">Action Verbs</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                            <div className="text-2xl font-bold text-indigo-600">{metrics.quantifiable_achievements}</div>
                            <div className="text-sm text-gray-600 mt-1">Metrics</div>
                        </div>
                    </div>
                </div>
            )}

            {/* Suggestions */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 analysis-anim">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className="text-2xl font-bold text-gray-900">
                            Enhancement Suggestions
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">
                            {total_suggestions} total suggestions • {critical_issues} critical issues
                        </p>
                    </div>
                    <div className="text-right">
                        <div className="text-sm text-gray-600">Selected</div>
                        <div className="text-2xl font-bold text-indigo-600">
                            {selectedSuggestions.length}/{total_suggestions}
                        </div>
                    </div>
                </div>

                {/* Grouped Suggestions by Category */}
                <div className="space-y-4">
                    {Object.entries(groupedSuggestions).map(([category, categorySuggestions]) => {
                        const Icon = categoryIcons[category];
                        const isExpanded = expandedCategory === category;

                        return (
                            <div key={category} className="border border-gray-200 rounded-lg overflow-hidden">
                                {/* Category Header */}
                                <button
                                    onClick={() => setExpandedCategory(isExpanded ? null : category)}
                                    className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                                >
                                    <div className="flex items-center space-x-3">
                                        <Icon className="w-5 h-5 text-indigo-600" />
                                        <span className="font-semibold text-gray-900">
                                            {categoryLabels[category]}
                                        </span>
                                        <span className="text-sm text-gray-500">
                                            ({categorySuggestions.length} issues)
                                        </span>
                                    </div>
                                    {isExpanded ? (
                                        <ChevronUp className="w-5 h-5 text-gray-600" />
                                    ) : (
                                        <ChevronDown className="w-5 h-5 text-gray-600" />
                                    )}
                                </button>

                                {/* Category Suggestions */}
                                {isExpanded && (
                                    <div className="p-4 space-y-3">
                                        {categorySuggestions.map((suggestion) => (
                                            <div
                                                key={suggestion.index}
                                                className={`border rounded-lg p-4 transition-all ${selectedSuggestions.includes(suggestion.index)
                                                    ? 'border-indigo-500 bg-indigo-50'
                                                    : 'border-gray-200 bg-white'
                                                    }`}
                                            >
                                                <div className="flex items-start space-x-3">
                                                    <input
                                                        type="checkbox"
                                                        checked={selectedSuggestions.includes(suggestion.index)}
                                                        onChange={() => handleToggleSuggestion(suggestion.index)}
                                                        className="mt-1 w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                                                    />
                                                    <div className="flex-1">
                                                        <div className="flex items-center justify-between mb-2">
                                                            <div className="flex items-center space-x-2">
                                                                {getSeverityBadge(suggestion.severity)}
                                                                <span className="text-xs font-medium text-gray-500">
                                                                    {suggestion.section}
                                                                </span>
                                                            </div>
                                                            {suggestion.enhanced_text && (
                                                                <Sparkles className="w-4 h-4 text-yellow-500" title="AI-Enhanced" />
                                                            )}
                                                        </div>

                                                        <div className="mb-2">
                                                            <div className="font-semibold text-gray-900 mb-1">
                                                                {suggestion.issue}
                                                            </div>
                                                            <div className="text-sm text-gray-700">
                                                                {suggestion.suggestion}
                                                            </div>
                                                        </div>

                                                        {/* Show enhanced text if available */}
                                                        {suggestion.enhanced_text && (
                                                            <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                                                                <div className="text-xs font-semibold text-green-800 mb-1">
                                                                    AI-Generated Enhancement:
                                                                </div>
                                                                <div className="text-sm text-gray-800">
                                                                    {suggestion.enhanced_text}
                                                                </div>
                                                            </div>
                                                        )}

                                                        {/* Show original text if it exists */}
                                                        {suggestion.original_text && (
                                                            <div className="mt-2 p-3 bg-gray-100 border border-gray-200 rounded-lg">
                                                                <div className="text-xs font-semibold text-gray-600 mb-1">
                                                                    Current Text:
                                                                </div>
                                                                <div className="text-sm text-gray-700">
                                                                    {suggestion.original_text}
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>

                {/* Action Buttons */}
                <div className="mt-6 flex items-center justify-between gap-4">
                    <div className="text-sm text-gray-600">
                        {selectedSuggestions.length === 0 ? (
                            'Select suggestions to apply to your resume'
                        ) : (
                            `${selectedSuggestions.length} enhancement${selectedSuggestions.length > 1 ? 's' : ''} selected`
                        )}
                    </div>
                    <button
                        onClick={() => onProceedToEnhance(selectedSuggestions)}
                        disabled={selectedSuggestions.length === 0}
                        className={`px-6 py-3 rounded-xl font-semibold text-white transition-all duration-200 ${selectedSuggestions.length === 0
                            ? 'bg-gray-300 cursor-not-allowed'
                            : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg transform hover:-translate-y-0.5'
                            }`}
                    >
                        Apply Selected Enhancements
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AnalysisResults;

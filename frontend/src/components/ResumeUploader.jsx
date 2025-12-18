import { useState, useCallback, useRef, useEffect } from 'react';
import { Upload, FileText, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import anime from 'animejs';

const ResumeUploader = ({ onUploadSuccess, isLoading, setIsLoading }) => {
    const [dragActive, setDragActive] = useState(false);
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const [uploadProgress, setUploadProgress] = useState(0);

    const containerRef = useRef(null);

    useEffect(() => {
        // Stagger animation for uploader elements
        if (containerRef.current) {
            anime({
                targets: containerRef.current.querySelectorAll('.uploader-anim'),
                translateY: [20, 0],
                opacity: [0, 1],
                delay: anime.stagger(100),
                easing: 'easeOutExpo',
                duration: 800
            });
        }
    }, []);

    const handleDrag = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    }, []);

    const validateFile = (selectedFile) => {
        setError('');

        // Check if file exists
        if (!selectedFile) {
            setError('Please select a file');
            return false;
        }

        // Check file type
        if (selectedFile.type !== 'application/pdf') {
            setError('Only PDF files are allowed');
            return false;
        }

        // Check file size (max 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB in bytes
        if (selectedFile.size > maxSize) {
            setError('File size must not exceed 5MB');
            return false;
        }

        if (selectedFile.size === 0) {
            setError('File is empty');
            return false;
        }

        return true;
    };

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const selectedFile = e.dataTransfer.files[0];
            if (validateFile(selectedFile)) {
                setFile(selectedFile);
            }
        }
    }, []);

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (validateFile(selectedFile)) {
                setFile(selectedFile);
            }
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file first');
            return;
        }

        console.log("Preparing to upload:", {
            name: file.name,
            size: file.size,
            type: file.type
        });

        setIsLoading(true);
        setError('');
        setUploadProgress(0);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const token = localStorage.getItem('access_token');

            // Simulate progress for better UX
            const progressInterval = setInterval(() => {
                setUploadProgress(prev => {
                    if (prev >= 90) {
                        clearInterval(progressInterval);
                        return prev;
                    }
                    return prev + 10;
                });
            }, 200);

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/api/v1/resume/analyze`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    // Note: Content-Type is NOT set here to allow browser to set boundary
                },
                body: formData,
            });

            clearInterval(progressInterval);
            setUploadProgress(100);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();

            console.log("Upload success! Received data:", data);

            // Call success callback
            onUploadSuccess(data);

            // Reset form
            setFile(null);
            setUploadProgress(0);
        } catch (err) {
            console.error("Upload error details:", err);
            setError(err.message || 'An error occurred during upload');
            setUploadProgress(0);
        } finally {
            setIsLoading(false);
        }
    };

    const removeFile = () => {
        setFile(null);
        setError('');
        setUploadProgress(0);
    };

    return (
        <div className="w-full max-w-2xl mx-auto" ref={containerRef}>
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                <div className="mb-6 uploader-anim ">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        Upload Your Resume for Analysis
                    </h2>
                    <p className="text-gray-600">
                        Get AI-powered insights and suggestions to improve your resume
                    </p>
                </div>

                {/* Drag and Drop Area */}
                <div
                    className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 uploader-anim  ${dragActive
                        ? 'border-indigo-500 bg-indigo-50'
                        : file
                            ? 'border-green-500 bg-green-50'
                            : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <input
                        type="file"
                        id="file-upload"
                        className="hidden"
                        accept=".pdf"
                        onChange={handleChange}
                        disabled={isLoading}
                    />

                    {!file ? (
                        <label htmlFor="file-upload" className="cursor-pointer">
                            <div className="flex flex-col items-center">
                                <Upload className="w-16 h-16 text-indigo-500 mb-4" />
                                <p className="text-lg font-semibold text-gray-700 mb-2">
                                    Drag & drop your resume here
                                </p>
                                <p className="text-sm text-gray-500 mb-4">
                                    or click to browse files
                                </p>
                                <p className="text-xs text-gray-400">
                                    PDF only • Max 5MB
                                </p>
                            </div>
                        </label>
                    ) : (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <FileText className="w-10 h-10 text-green-500" />
                                <div className="text-left">
                                    <p className="font-semibold text-gray-900">{file.name}</p>
                                    <p className="text-sm text-gray-500">
                                        {(file.size / 1024 / 1024).toFixed(2)} MB
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={removeFile}
                                disabled={isLoading}
                                className="p-2 hover:bg-red-50 rounded-full transition-colors disabled:opacity-50"
                            >
                                <XCircle className="w-6 h-6 text-red-500" />
                            </button>
                        </div>
                    )}
                </div>

                {/* Upload Progress */}
                {uploadProgress > 0 && uploadProgress < 100 && (
                    <div className="mt-4 uploader-anim">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">Analyzing...</span>
                            <span className="text-sm font-medium text-indigo-600">{uploadProgress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                                className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300"
                                style={{ width: `${uploadProgress}%` }}
                            ></div>
                        </div>
                    </div>
                )}

                {/* Error Message */}
                {error && (
                    <div className="mt-4 flex items-center p-4 bg-red-50 border border-red-200 rounded-lg uploader-anim">
                        <AlertCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
                        <p className="text-sm text-red-700">{error}</p>
                    </div>
                )}

                {/* Success Message */}
                {uploadProgress === 100 && !error && (
                    <div className="mt-4 flex items-center p-4 bg-green-50 border border-green-200 rounded-lg uploader-anim">
                        <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                        <p className="text-sm text-green-700">Resume analyzed successfully!</p>
                    </div>
                )}

                {/* Upload Button */}
                <div className="uploader-anim ">
                    <button
                        onClick={handleUpload}
                        disabled={!file || isLoading}
                        className={`w-full mt-6 py-3 px-6 rounded-xl font-semibold text-white transition-all duration-200 ${!file || isLoading
                            ? 'bg-gray-300 cursor-not-allowed'
                            : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg transform hover:-translate-y-0.5'
                            }`}
                    >
                        {isLoading ? (
                            <span className="flex items-center justify-center">
                                <svg
                                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                >
                                    <circle
                                        className="opacity-25"
                                        cx="12"
                                        cy="12"
                                        r="10"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                    ></circle>
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    ></path>
                                </svg>
                                Analyzing Resume...
                            </span>
                        ) : (
                            'Analyze Resume'
                        )}
                    </button>
                </div>

                {/* Info */}
                <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg uploader-anim ">
                    <p className="text-xs text-blue-700">
                        <strong>What we analyze:</strong> Content quality, ATS optimization, structure,
                        and fresher-specific aspects to help you create a winning resume.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ResumeUploader;

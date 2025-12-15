/**
 * Home/Landing Page
 */
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/store';
import Button from '../components/Button';

export default function Home() {
    const { isAuthenticated } = useAuthStore();

    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            <section className="py-20 px-4">
                <div className="max-w-6xl mx-auto text-center">
                    <div className="mb-8">
                        <span className="inline-block px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-semibold mb-6">
                            🚀 AI-Powered Resume Builder for Freshers
                        </span>
                    </div>

                    <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
                        Build Your Dream Resume
                        <br />
                        <span className="gradient-text">With AI Assistance</span>
                    </h1>

                    <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-10">
                        Transform your raw experience into professional, ATS-optimized resume content.
                        Perfect for students and freshers entering the job market.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                        {isAuthenticated ? (
                            <Link to="/dashboard">
                                <Button>Go to Dashboard</Button>
                            </Link>
                        ) : (
                            <>
                                <Link to="/register">
                                    <Button>Get Started Free</Button>
                                </Link>
                                <Link to="/pricing">
                                    <Button variant="secondary">View Pricing</Button>
                                </Link>
                            </>
                        )}
                    </div>

                    <p className="text-sm text-gray-500 mt-4">
                        ✨ No credit card required • 3 free AI improvements
                    </p>
                </div>
            </section>

            {/* Features Grid */}
            <section className="py-20 px-4 bg-white/50">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-4xl font-bold text-center mb-12">
                        Why Choose <span className="gradient-text">AI Resume Coach</span>?
                    </h2>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="card text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-bold mb-2">AI-Powered</h3>
                            <p className="text-gray-600">
                                Smart AI converts your informal input into professional, ATS-friendly content
                            </p>
                        </div>

                        <div className="card text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-accent-100 to-accent-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <svg className="w-8 h-8 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-bold mb-2">Secure & Private</h3>
                            <p className="text-gray-600">
                                Enterprise-grade security with encrypted data and rate limiting
                            </p>
                        </div>

                        <div className="card text-center">
                            <div className="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-bold mb-2">ATS-Optimized</h3>
                            <p className="text-gray-600">
                                Clean, professional formatting that passes applicant tracking systems
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Tier Comparison */}
            <section className="py-20 px-4">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-4xl font-bold text-center mb-4">
                        Simple, Transparent Pricing
                    </h2>
                    <p className="text-gray-600 text-center mb-12">
                        Start free, upgrade when you need more power
                    </p>

                    <div className="grid md:grid-cols-3 gap-6">
                        <div className="pricing-card">
                            <h3 className="text-xl font-bold mb-2">FREE</h3>
                            <div className="text-3xl font-bold mb-4">$0</div>
                            <p className="text-sm text-gray-600 mb-4">Perfect for trying out</p>
                            <ul className="space-y-2 text-sm">
                                <li>✅ 3 AI improvements</li>
                                <li>✅ 1 resume</li>
                                <li>✅ Basic template</li>
                                <li>⚠️ Watermarked PDF</li>
                            </ul>
                        </div>

                        <div className="pricing-card-popular">
                            <h3 className="text-xl font-bold mb-2">PRO</h3>
                            <div className="text-3xl font-bold mb-4">$9.99<span className="text-sm font-normal">/mo</span></div>
                            <p className="text-sm text-gray-600 mb-4">For serious job seekers</p>
                            <ul className="space-y-2 text-sm">
                                <li>✅ 50 AI actions/month</li>
                                <li>✅ 10 resumes</li>
                                <li>✅ All templates</li>
                                <li>✅ No watermark</li>
                                <li>✅ Project generation</li>
                            </ul>
                        </div>

                        <div className="pricing-card">
                            <h3 className="text-xl font-bold mb-2">ULTIMATE</h3>
                            <div className="text-3xl font-bold mb-4">$19.99<span className="text-sm font-normal">/mo</span></div>
                            <p className="text-sm text-gray-600 mb-4">Unlimited power</p>
                            <ul className="space-y-2 text-sm">
                                <li>✅ Unlimited AI</li>
                                <li>✅ Unlimited resumes</li>
                                <li>✅ All templates</li>
                                <li>✅ Advanced tone control</li>
                                <li>✅ Priority processing</li>
                            </ul>
                        </div>
                    </div>

                    <div className="text-center mt-8">
                        <Link to="/pricing">
                            <Button variant="primary">View Full Pricing Details</Button>
                        </Link>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-4 bg-gradient-to-r from-primary-600 to-accent-600">
                <div className="max-w-4xl mx-auto text-center text-white">
                    <h2 className="text-4xl font-bold mb-4">
                        Ready to Build Your Perfect Resume?
                    </h2>
                    <p className="text-xl mb-8 opacity-90">
                        Join thousands of freshers landing their dream jobs
                    </p>
                    <Link to="/register">
                        <Button className="bg-white text-primary-700 hover:bg-gray-100">
                            Get Started for Free
                        </Button>
                    </Link>
                </div>
            </section>
        </div>
    );
}

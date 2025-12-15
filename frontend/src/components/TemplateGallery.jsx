import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

const TemplateGallery = ({ onSelectTemplate, currentTemplateId }) => {
    const [templates, setTemplates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState({
        industry: '',
        position_type: '',
        category: ''
    });
    const [industries, setIndustries] = useState([]);
    const [categories, setCategories] = useState([]);
    const [positionTypes, setPositionTypes] = useState([]);

    useEffect(() => {
        fetchFilterOptions();
        fetchTemplates();
    }, []);

    useEffect(() => {
        fetchTemplates();
    }, [filter]);

    const fetchFilterOptions = async () => {
        try {
            const [indResp, catResp, posResp] = await Promise.all([
                api.get('/templates/industries/list'),
                api.get('/templates/categories/list'),
                api.get('/templates/position-types/list')
            ]);
            setIndustries(indResp.data.industries);
            setCategories(catResp.data.categories);
            setPositionTypes(posResp.data.position_types);
        } catch (error) {
            console.error('Error fetching filter options:', error);
        }
    };

    const fetchTemplates = async () => {
        setLoading(true);
        try {
            const params = {};
            if (filter.industry) params.industry = filter.industry;
            if (filter.position_type) params.position_type = filter.position_type;
            if (filter.category) params.category = filter.category;

            const response = await api.get('/templates', { params });
            setTemplates(response.data.templates);
        } catch (error) {
            console.error('Error fetching templates:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleTemplateSelect = async (template) => {
        // Check if template is available in user's tier
        const userCanAccess = await checkTemplateAccess(template);

        if (!userCanAccess) {
            alert(`This template requires ${template.tier_required} plan. Please upgrade!`);
            return;
        }

        // Increment usage count
        try {
            await api.post(`/templates/${template.id}/increment-usage`);
        } catch (error) {
            console.error('Error incrementing usage:', error);
        }

        onSelectTemplate(template);
    };

    const checkTemplateAccess = async (template) => {
        // This would check against user's current plan
        // For now, returning true - implement tier check in production
        return true;
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
            </div>
        );
    }

    return (
        <div className="template-gallery">
            {/* Filters */}
            <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label className="block text-sm font-medium mb-2">Industry</label>
                    <select
                        value={filter.industry}
                        onChange={(e) => setFilter({ ...filter, industry: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                        <option value="">All Industries</option>
                        {industries.map((ind) => (
                            <option key={ind} value={ind}>{ind}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium mb-2">Position Level</label>
                    <select
                        value={filter.position_type}
                        onChange={(e) => setFilter({ ...filter, position_type: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                        <option value="">All Levels</option>
                        {positionTypes.map((pos) => (
                            <option key={pos} value={pos}>{pos}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium mb-2">Category</label>
                    <select
                        value={filter.category}
                        onChange={(e) => setFilter({ ...filter, category: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                        <option value="">All Categories</option>
                        {categories.map((cat) => (
                            <option key={cat} value={cat}>{cat}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Template Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {templates.map((template) => (
                    <div
                        key={template.id}
                        className={`border-2 rounded-lg p-4 cursor-pointer transition-all hover:shadow-lg ${currentTemplateId === template.id
                                ? 'border-purple-600 bg-purple-50'
                                : 'border-gray-200 hover:border-purple-400'
                            }`}
                        onClick={() => handleTemplateSelect(template)}
                    >
                        {/* Featured Badge */}
                        {template.is_featured && (
                            <div className="inline-block bg-yellow-400 text-yellow-900 text-xs px-2 py-1 rounded-full mb-2">
                                ⭐ Featured
                            </div>
                        )}

                        {/* Tier Badge */}
                        <div className={`inline-block ml-2 text-xs px-2 py-1 rounded-full ${template.tier_required === 'FREE'
                                ? 'bg-green-100 text-green-800'
                                : template.tier_required === 'PRO'
                                    ? 'bg-blue-100 text-blue-800'
                                    : 'bg-purple-100 text-purple-800'
                            }`}>
                            {template.tier_required}
                        </div>

                        {/* Template Preview (placeholder) */}
                        <div className="mt-3 h-48 bg-gradient-to-br from-gray-100 to-gray-200 rounded flex items-center justify-center">
                            <span className="text-4xl">📄</span>
                        </div>

                        {/* Template Info */}
                        <h3 className="mt-4 font-bold text-lg">{template.display_name}</h3>
                        <p className="text-sm text-gray-600 mt-1">{template.description}</p>

                        <div className="mt-3 flex flex-wrap gap-2">
                            {template.industry && (
                                <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                                    {template.industry}
                                </span>
                            )}
                            {template.position_type && (
                                <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                                    {template.position_type}
                                </span>
                            )}
                            {template.category && (
                                <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                                    {template.category}
                                </span>
                            )}
                        </div>

                        {currentTemplateId === template.id && (
                            <div className="mt-3 text-purple-600 font-medium text-sm">
                                ✓ Currently Selected
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {templates.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                    No templates found. Try adjusting your filters.
                </div>
            )}
        </div>
    );
};

export default TemplateGallery;

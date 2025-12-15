# Contributing to AI Resume Coach

Thank you for considering contributing to AI Resume Coach! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

1. **Bug Reports**: Report bugs via GitHub Issues
2. **Feature Requests**: Suggest new features
3. **Code Contributions**: Submit Pull Requests
4. **Documentation**: Improve docs
5. **Testing**: Write tests

## 🚀 Getting Started

### 1. Fork the Repository

Click "Fork" on GitHub to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-coach.git
cd ai-resume-coach
```

### 3. Set Up Development Environment

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
# Configure .env
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## 📋 Coding Standards

### Backend (Python)

- **Style**: Follow PEP 8
- **Type Hints**: Use type hints where possible
- **Docstrings**: Add docstrings to all functions
- **Error Handling**: Use try-except appropriately

**Example:**
```python
def create_resume(resume_data: ResumeCreate, user: User, db: Session) -> Resume:
    """
    Create a new resume for the user.
    
    Args:
        resume_data: Resume creation data
        user: Current authenticated user
        db: Database session
        
    Returns:
        Created resume object
        
    Raises:
        HTTPException: If resume limit reached
    """
    # Implementation
```

### Frontend (React/JavaScript)

- **Style**: Use Prettier/ESLint
- **Components**: Functional components with hooks
- **Naming**: PascalCase for components, camelCase for functions
- **Comments**: Explain complex logic

**Example:**
```jsx
/**
 * AI chat interface component
 * @param {Object} props - Component props
 * @param {string} props.resumeId - Current resume ID
 */
export default function AIChat({ resumeId }) {
  // Implementation
}
```

## 🔧 Development Workflow

### 1. Make Changes

- Keep changes focused and atomic
- Write clean, readable code
- Add comments where necessary

### 2. Test Your Changes

**Backend:**
```bash
# Run server
uvicorn app.main:app --reload

# Test manually or write unit tests
pytest  # If tests are added
```

**Frontend:**
```bash
# Run dev server
npm run dev

# Test in browser
```

### 3. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: Add advanced tone control for ULTIMATE tier"
git commit -m "fix: Resolve PDF watermark positioning issue"
git commit -m "docs: Update payment integration guide"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build tasks, etc.

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Describe your changes
5. Submit PR

## 📝 Pull Request Guidelines

### PR Title
Use conventional commit format:
- `feat: Add LinkedIn import feature`
- `fix: Resolve tier limit reset bug`

### PR Description
Include:
- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How was it tested?

**Template:**
```markdown
## Description
Added LinkedIn profile import feature for PRO and ULTIMATE tiers.

## Motivation
Users requested the ability to import LinkedIn data to speed up resume creation.

## Changes
- Added LinkedIn API integration
- Created import UI component
- Updated tier service to check import feature access

## Testing
- Tested with multiple LinkedIn profiles
- Verified tier-based access control
- Checked error handling for invalid profiles

## Screenshots
[If applicable]
```

## 🧪 Testing Guidelines

### Manual Testing Checklist

- [ ] Feature works as expected
- [ ] Tier enforcement working correctly
- [ ] Error handling graceful
- [ ] UI responsive on mobile
- [ ] No console errors
- [ ] API responses correct

### Writing Tests (Future)

When adding tests:
- Use `pytest` for backend
- Use React Testing Library for frontend
- Coverage should be >80%

## 🎨 UI/UX Contributions

### Design Principles
- **Clean & Modern**: Follow existing design system
- **Accessible**: WCAG 2.1 AA compliance
- **Responsive**: Mobile-first approach
- **Consistent**: Use existing components

### Before Submitting UI Changes
- Test on mobile, tablet, desktop
- Check dark mode compatibility (if implemented)
- Ensure accessibility (keyboard navigation, screen readers)

## 🔒 Security Contributions

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security contact (if provided)
2. Describe the vulnerability
3. Wait for acknowledgment before disclosure

### Security Checklist for PRs

- [ ] No hardcoded secrets
- [ ] Input validation added
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF tokens (if form submission)

## 📚 Documentation Contributions

### What to Document
- New features
- API endpoint changes
- Configuration options
- Deployment procedures

### Documentation Style
- Clear and concise
- Include code examples
- Add screenshots for UI features
- Update README if significant change

## 🏗 Architecture Guidelines

### Adding New Features

1. **Backend First**: Implement API endpoint
2. **Tier Check**: Add tier enforcement if needed
3. **Frontend**: Build UI components
4. **Integration**: Connect frontend to backend
5. **Documentation**: Update docs

### Modifying Tier System

**⚠️ CRITICAL**: Tier logic must stay in backend.

- **DO**: Add new tiers in `PlanTier` enum
- **DO**: Update `tier_service.py`
- **DO**: Update frontend only for UI display
- **DON'T**: Enforce limits in frontend only

### Adding Payment Providers

See `PAYMENT_INTEGRATION.md` for detailed guide.

1. Add SDK to `requirements.txt`
2. Update `billing.py` endpoints
3. Add webhook handler
4. Update frontend payment flow
5. Test in sandbox mode

## 🐛 Bug Fix Process

1. **Reproduce**: Confirm bug exists
2. **Identify**: Find root cause
3. **Fix**: Implement solution
4. **Test**: Verify fix works
5. **Document**: Update changelog

## 📊 Feature Request Process

1. **Check Existing**: Search for similar requests
2. **Describe**: Clear description of feature
3. **Use Case**: Why is it needed?
4. **Mockups**: Add designs if UI feature

## ⚖️ Code of Conduct

### Our Standards
- **Respectful**: Be kind and professional
- **Constructive**: Provide helpful feedback
- **Collaborative**: Work together
- **Inclusive**: Welcome all contributors

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Personal attacks
- Spam or off-topic content

## 🎁 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Questions?

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bug reports
- **Pull Requests**: For code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AI Resume Coach!** 🚀

Your contributions help make this product better for everyone.

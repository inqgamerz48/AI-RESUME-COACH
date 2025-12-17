#!/bin/bash

# 🚀 GitHub Push Helper Script
# This script helps you push your project to GitHub safely

echo "🎉 AI Resume Coach - GitHub Push Helper"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Project directory verified${NC}"
echo ""

# Security check - look for sensitive files
echo "🔒 Running security checks..."
echo ""

# Check if .env files would be committed
if git check-ignore frontend/.env backend/.env > /dev/null 2>&1; then
    echo -e "${GREEN}✅ .env files are properly ignored${NC}"
else
    echo -e "${RED}⚠️  WARNING: .env files might be committed!${NC}"
    echo "   Please check your .gitignore file"
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for test databases
if git check-ignore backend/test.db > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database files are properly ignored${NC}"
else
    echo -e "${YELLOW}⚠️  No test.db file found or not ignored${NC}"
fi

# Search for potential secrets in code
echo ""
echo "Scanning for potential secrets..."
if grep -r "sk_test" --exclude-dir={venv,node_modules,.git} --exclude="*.md" --exclude="*.sh" . > /dev/null 2>&1; then
    echo -e "${RED}⚠️  WARNING: Found potential Stripe test keys in code${NC}"
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if grep -r "sk_live" --exclude-dir={venv,node_modules,.git} --exclude="*.md" --exclude="*.sh" . > /dev/null 2>&1; then
    echo -e "${RED}🚨 DANGER: Found potential Stripe LIVE keys in code!${NC}"
    echo "   DO NOT COMMIT THIS!"
    exit 1
fi

echo -e "${GREEN}✅ Security checks passed${NC}"
echo ""
echo "========================================"
echo ""

# Get repository information
echo "📝 GitHub Repository Setup"
echo ""
read -p "Enter your GitHub username: " GITHUB_USER
read -p "Enter repository name (e.g., ai-resume-coach): " REPO_NAME
echo ""

# Confirm
echo "Repository will be created at:"
echo -e "${YELLOW}https://github.com/$GITHUB_USER/$REPO_NAME${NC}"
echo ""
read -p "Is this correct? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo ""
    echo "🔧 Initializing git repository..."
    git init
    echo -e "${GREEN}✅ Git initialized${NC}"
fi

# Show what will be committed
echo ""
echo "📦 Files to be committed:"
echo ""
git add -A --dry-run | head -20
echo "... and more files"
echo ""

read -p "Review looks good? Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled. No files were committed."
    exit 1
fi

# Add all files
echo ""
echo "📦 Adding files to git..."
git add .
echo -e "${GREEN}✅ Files added${NC}"

# Create commit
echo ""
echo "💾 Creating commit..."
git commit -m "🎉 Initial commit: AI Resume Coach MVP v1.0.0

- Complete full-stack SaaS application
- 3-tier monetization system (FREE/PRO/ULTIMATE)
- AI-powered resume improvement
- Enterprise-grade security
- Payment-ready infrastructure
- Comprehensive documentation
- Modern React + FastAPI stack"

echo -e "${GREEN}✅ Commit created${NC}"

# Rename branch to main
git branch -M main

# Add remote
echo ""
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo -e "${GREEN}✅ Remote added${NC}"

# Show next steps
echo ""
echo "========================================"
echo -e "${GREEN}✅ Git repository ready!${NC}"
echo "========================================"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Create the repository on GitHub:"
echo "   👉 https://github.com/new"
echo "   - Name: $REPO_NAME"
echo "   - Description: 🚀 AI-Powered Resume Coach - Production-ready SaaS MVP"
echo "   - Choose Public or Private"
echo "   - DO NOT initialize with README, .gitignore, or license"
echo ""
echo "2. After creating the repository, push your code:"
echo "   ${YELLOW}git push -u origin main${NC}"
echo ""
echo "3. If you have GitHub CLI installed, you can create and push in one command:"
echo "   ${YELLOW}gh repo create $REPO_NAME --public --source=. --remote=origin --push${NC}"
echo ""
echo "========================================"
echo ""
echo "📚 For detailed instructions, see GITHUB_SETUP.md"
echo ""
echo "🎉 Good luck with your project!"

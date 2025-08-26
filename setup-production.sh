#!/bin/bash

# Production Setup Script for Vibe Code Reviewer
echo "🚀 Setting up Vibe Code Reviewer for Production..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run ./start.sh first to create it."
    exit 1
fi

echo "📝 Configuring for production with Google Gemini..."

# Update .env file for production
sed -i.bak 's/LLM_PROVIDER=ollama/LLM_PROVIDER=google/' .env
sed -i.bak 's/LLM_MODEL=deepseek-coder:1.3b/LLM_MODEL=gemini-2.0-flash-exp/' .env

echo "✅ Updated .env file for production:"
echo "   LLM_PROVIDER=google"
echo "   LLM_MODEL=gemini-2.0-flash-exp"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your GOOGLE_API_KEY"
echo "2. Run: docker-compose up --build -d"
echo "3. Access the application at http://localhost:3000"
echo ""
echo "🔧 To switch back to local development:"
echo "   sed -i 's/LLM_PROVIDER=google/LLM_PROVIDER=ollama/' .env"
echo "   sed -i 's/LLM_MODEL=gemini-2.0-flash-exp/LLM_MODEL=deepseek-coder:1.3b/' .env"

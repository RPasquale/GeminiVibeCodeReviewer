#!/bin/bash

# Vibe Code Reviewer Startup Script
echo "🚀 Starting Vibe Code Reviewer..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "   You can find the file at: $(pwd)/.env"
    read -p "Press Enter after you've configured your API keys..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/data
mkdir -p backend/models

# Build and start containers
echo "🐳 Building and starting containers..."
docker-compose up --build -d

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
sleep 15

# Download the deepseek-coder model if using Ollama
if grep -q "LLM_PROVIDER=ollama" .env; then
    echo "🤖 Downloading deepseek-coder:1.3b model..."
    docker-compose exec -T ollama ollama pull deepseek-coder:1.3b
    
    if [ $? -eq 0 ]; then
        echo "✅ deepseek-coder:1.3b model downloaded successfully"
    else
        echo "❌ Failed to download deepseek-coder:1.3b model"
        echo "   You can manually download it later with:"
        echo "   docker-compose exec ollama ollama pull deepseek-coder:1.3b"
    fi
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check backend health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

# Check frontend health
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi

# Check MLflow
if curl -f http://localhost:5000 > /dev/null 2>&1; then
    echo "✅ MLflow is healthy"
else
    echo "❌ MLflow health check failed"
fi

# Check Ollama
if curl -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is healthy"
else
    echo "❌ Ollama health check failed"
fi

echo ""
echo "🎉 Vibe Code Reviewer is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 MLflow: http://localhost:5000"
echo "🤖 Ollama: http://localhost:11434"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the application, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"
echo ""
echo "For Ollama model management:"
echo "  List models: docker-compose exec ollama ollama list"
echo "  Pull new model: docker-compose exec ollama ollama pull <model-name>"
echo "  Remove model: docker-compose exec ollama ollama rm <model-name>"

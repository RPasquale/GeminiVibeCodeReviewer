# DSPy Code Reviewer 🚀

An advanced code review system powered by [DSPy](https://github.com/stanfordnlp/dspy) framework, featuring comprehensive AI-powered code analysis, RAG capabilities, multi-hop reasoning, and continuous optimization.

## 🌟 Features

### Core Functionality
- **Advanced Code Review**: Comprehensive analysis using DSPy's optimized LLM pipelines
- **RAG (Retrieval-Augmented Generation)**: Context-aware code analysis with document retrieval
- **Multi-Hop Reasoning**: Complex reasoning for sophisticated code analysis
- **Batch Processing**: Review multiple files with cross-file analysis
- **Real-time Optimization**: Continuous improvement using DSPy's optimization algorithms

### AI/ML Capabilities
- **Prompt Optimization**: Bootstrap few-shot and random search optimization
- **Model Training**: Fine-tuning pipelines for specialized code review tasks
- **Hyperparameter Tuning**: Automated optimization of model parameters
- **Performance Analysis**: Detailed analysis and optimization recommendations
- **Model Comparison**: Comprehensive evaluation of different models

### Infrastructure
- **Containerized Architecture**: Docker-based frontend and backend
- **Scalable Backend**: FastAPI with async support
- **Vector Database**: Document storage and retrieval
- **Experiment Tracking**: MLflow integration for model management
- **Monitoring**: Comprehensive logging and health checks

### LLM Provider Support
- **Local Development**: Ollama with deepseek-coder:1.3b model
- **Production**: Google Gemini, OpenAI GPT, Anthropic Claude
- **Easy Switching**: Simple configuration to switch between providers

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   MLflow        │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Tracking)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   (Database)    │
                       │   Port: 5432    │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Cache)       │
                       │   Port: 6379    │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Ollama       │
                       │   (Local LLM)   │
                       │   Port: 11434   │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- For production: API keys for OpenAI, Anthropic, or Google (at least one)
- For local development: No API keys required (uses Ollama)

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd VibeCodeReviewer
```

### 2. Configure Environment
```bash
cp env.example .env
# Edit .env with your preferred LLM provider
```

### 3. Start the Application
```bash
./start.sh
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MLflow**: http://localhost:5000
- **Ollama**: http://localhost:11434

## 🔧 LLM Provider Configuration

### Local Development (Default)
```bash
# Uses Ollama with deepseek-coder:1.3b
LLM_PROVIDER=ollama
LLM_MODEL=deepseek-coder:1.3b
OLLAMA_BASE_URL=http://localhost:11434
```

### Production with Google Gemini
```bash
# Uses Google Gemini
LLM_PROVIDER=google
LLM_MODEL=gemini-2.0-flash-exp
GOOGLE_API_KEY=your_google_api_key
```

### Production with OpenAI
```bash
# Uses OpenAI GPT
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
OPENAI_API_KEY=your_openai_api_key
```

### Production with Anthropic
```bash
# Uses Anthropic Claude
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### Quick Provider Switching
```bash
# Switch to production (Gemini)
./setup-production.sh

# Switch back to local development
sed -i 's/LLM_PROVIDER=google/LLM_PROVIDER=ollama/' .env
sed -i 's/LLM_MODEL=gemini-2.0-flash-exp/LLM_MODEL=deepseek-coder:1.3b/' .env
```

## 📚 API Endpoints

### Code Review
- `POST /api/v1/code-review/review` - Review single code file
- `POST /api/v1/code-review/review/batch` - Review multiple files
- `POST /api/v1/code-review/optimize` - Optimize code reviewer
- `GET /api/v1/code-review/status` - Get system status

### RAG (Retrieval-Augmented Generation)
- `POST /api/v1/rag/query` - Perform RAG query
- `POST /api/v1/rag/search` - Vector search
- `POST /api/v1/rag/ingest` - Ingest documents
- `POST /api/v1/rag/multi-hop` - Multi-hop reasoning

### Training & Optimization
- `POST /api/v1/training/start` - Start training job
- `GET /api/v1/training/status/{id}` - Get training progress
- `POST /api/v1/optimization/start` - Start optimization
- `GET /api/v1/optimization/results/{id}` - Get optimization results

### Models
- `GET /api/v1/models/info` - Get model information
- `GET /api/v1/models/available` - List available models
- `POST /api/v1/models/switch` - Switch models
- `GET /api/v1/models/capabilities` - Get model capabilities

## 🔧 Configuration

### Environment Variables
```bash
# LLM Configuration
LLM_PROVIDER=ollama  # Options: "ollama", "openai", "anthropic", "google"
LLM_MODEL=deepseek-coder:1.3b  # Model name for the selected provider

# Ollama Configuration (for local development)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-coder:1.3b

# API Keys (for production providers)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/dspy_app

# Redis
REDIS_URL=redis://localhost:6379

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# DSPy Configuration
DSPY_MAX_TOKENS=4000
DSPY_TEMPERATURE=0.1
```

## 🧪 DSPy Integration

This project leverages DSPy's powerful capabilities:

### Core DSPy Features
- **Signatures**: Structured input/output definitions
- **Modules**: Reusable AI components (Predict, ChainOfThought, ReAct)
- **Optimizers**: Bootstrap few-shot, random search, Bayesian optimization
- **Evaluation**: Comprehensive metrics and assessment

### Supported Tasks
1. **Code Review**: Comprehensive analysis with feedback categorization
2. **RAG**: Document retrieval and context-aware generation
3. **Multi-Hop Reasoning**: Complex reasoning chains
4. **Classification**: Code categorization and analysis
5. **Optimization**: Continuous improvement of prompts and models

## 🛠️ Development

### Local Development Setup
```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
npm install
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
npm test
```

### Code Quality
```bash
# Backend
cd backend
black .
flake8 .
mypy .

# Frontend
npm run lint
npm run format
```

## 📊 Monitoring and Logging

### Health Checks
- Backend: `GET /health`
- Model: `GET /api/v1/models/health`
- Database: Automatic connection monitoring
- Ollama: `GET http://localhost:11434/api/tags`

### Logging
- Application logs: `backend/logs/app.log`
- Docker logs: `docker-compose logs -f`
- MLflow tracking: http://localhost:5000

## 🔄 Continuous Optimization

The system continuously improves through:

1. **Feedback Collection**: User feedback on code reviews
2. **Performance Analysis**: Automatic bottleneck detection
3. **Model Optimization**: DSPy-based prompt and weight optimization
4. **A/B Testing**: Model comparison and selection
5. **Hyperparameter Tuning**: Automated parameter optimization

## 🤖 Ollama Management

### Model Operations
```bash
# List available models
docker-compose exec ollama ollama list

# Pull a new model
docker-compose exec ollama ollama pull codellama:7b

# Remove a model
docker-compose exec ollama ollama rm deepseek-coder:1.3b

# Run a model directly
docker-compose exec ollama ollama run deepseek-coder:1.3b
```

### Supported Models for Code Review
- `deepseek-coder:1.3b` (default, optimized for code)
- `codellama:7b` (good balance of performance and speed)
- `codellama:13b` (higher quality, slower)
- `wizardcoder:7b` (excellent code generation)
- `phind-codellama:7b` (optimized for coding tasks)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [DSPy Team](https://github.com/stanfordnlp/dspy) for the amazing framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
- [MLflow](https://mlflow.org/) for experiment tracking
- [Ollama](https://ollama.ai/) for local LLM inference

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at http://localhost:8000/docs
- Review the DSPy documentation at https://dspy.ai

---

**Built with ❤️ using DSPy for advanced AI-powered code review**

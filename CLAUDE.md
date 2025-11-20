# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a hackathon project for building a ChatGPT-style chat application. The repository is currently empty and ready for initial development.

## Expected Technology Stack

Based on the repository name and hackathon context, this project will likely involve:

### Frontend Options
- **React/Next.js**: For building interactive chat interfaces
- **Vue.js**: Alternative frontend framework
- **Vanilla JavaScript**: For simple implementations

### Backend Options
- **Node.js/Express**: For API server and WebSocket connections
- **Python/FastAPI**: For AI integration and API endpoints
- **Python/Flask**: Lightweight web framework option

### AI Integration
- **OpenAI API**: For ChatGPT integration
- **Anthropic Claude API**: For Claude integration
- **Local LLM**: For self-hosted solutions

## Common Development Commands

### Node.js/React Projects
```bash
# Initialize project
npm init -y
npm install

# Development server
npm run dev
npm start

# Testing
npm test
npm run test:watch

# Build for production
npm run build

# Linting and formatting
npm run lint
npm run prettier
```

### Python Projects
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run application
python app.py
python -m uvicorn main:app --reload  # For FastAPI

# Testing
pytest
python -m pytest tests/

# Code quality
black .
flake8
```

### Docker Development
```bash
# Build container
docker build -t chat-app .

# Run locally
docker run -p 3000:3000 chat-app
docker run -p 8000:8000 chat-app  # For Python apps

# Docker Compose
docker-compose up
docker-compose up --build
```

## Architecture Patterns for Chat Applications

### Real-time Communication
- **WebSockets**: For live chat functionality
- **Server-Sent Events (SSE)**: For streaming AI responses
- **Polling**: Simple fallback for real-time updates

### State Management
- **Frontend State**: React Context, Redux, or Zustand for chat history
- **Backend State**: Session management and conversation persistence
- **Database**: Chat history, user preferences, conversation threads

### API Integration Patterns
- **Streaming Responses**: Handle chunked AI responses for better UX
- **Rate Limiting**: Prevent API quota exhaustion
- **Error Handling**: Graceful fallbacks for API failures
- **Authentication**: Secure API key management

### Common Chat Features
- **Message History**: Persistent conversation storage
- **User Authentication**: Login/signup functionality
- **Multiple Conversations**: Thread/session management
- **Export/Share**: Conversation sharing capabilities
- **Customization**: Themes, settings, AI model selection

## Environment Setup

### Required Environment Variables
```bash
# AI API Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here

# Database Configuration
DATABASE_URL=your_database_connection_string

# Application Configuration
PORT=3000
NODE_ENV=development
```

### Security Considerations
- Never commit API keys to version control
- Use environment variables for all sensitive configuration
- Implement proper API key rotation
- Add rate limiting to prevent abuse
- Sanitize user inputs to prevent XSS attacks

## Development Workflow

### Initial Setup
1. Choose technology stack (React + Node.js recommended for hackathons)
2. Set up basic project structure
3. Configure environment variables
4. Implement basic chat UI
5. Integrate AI API
6. Add real-time communication
7. Implement persistence

### Testing Strategy
- **Unit Tests**: Core logic and utilities
- **Integration Tests**: API endpoints and AI integration
- **E2E Tests**: Full chat workflow testing
- **Manual Testing**: UI/UX validation

### Deployment Options
- **Vercel/Netlify**: For frontend-only or full-stack Next.js
- **Heroku**: Simple full-stack deployment
- **Railway/Render**: Modern alternatives to Heroku
- **Docker**: Containerized deployment to any platform
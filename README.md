# Jenkins AI Chatbot — GSoC 2026

## Project Overview
A complete AI-powered chatbot system for Jenkins that assists users with workflow guidance, build log analysis, documentation retrieval, plugin recommendations, and pipeline code generation using LLMs and RAG architecture.

### Architecture Diagram (Text-Based)

```
+---------------------+      +---------------------+      +---------------------+
| Jenkins Plugin (UI) |<---> | FastAPI Backend     |<---> | FAISS Vector Store  |
| (Java, Jelly)       |      | (Python, LangChain) |      | (Docs, Embeddings)  |
+---------------------+      +---------------------+      +---------------------+
		  |                        |                        |
		  |                        |                        |
		  v                        v                        v
+---------------------+      +---------------------+      +---------------------+
| Jenkins REST API    |      | LLM Providers       |      | Ollama Service      |
| (Live Data)         |      | (OpenAI, Gemini,    |      | (Local LLM)         |
|                     |      |  Ollama)            |      |                     |
+---------------------+      +---------------------+      +---------------------+
```

## Prerequisites
- Python 3.11+
- Java 11+
- Maven
- Docker

## Quick Start Guide
1. **Clone the repository:**
	```bash
	git clone https://github.com/im-alok74/jenkins-doc-chatbot.git
	cd jenkins-doc-chatbot
	```
2. **Set up environment variables:**
	- Copy `.env.example` to `.env` and fill in your API keys and Jenkins details.
3. **Index Jenkins documentation:**
	```bash
	python jenkins-chatbot-backend/scripts/index_docs.py
	```
4. **Run backend and Ollama with Docker Compose:**
	```bash
	docker-compose up --build
	```
	Or run backend directly:
	```bash
	uvicorn jenkins-chatbot-backend.main:app --host 0.0.0.0 --port 8000
	```
5. **Build Jenkins plugin:**
	```bash
	cd jenkins-chatbot-plugin
	mvn package
	```
6. **Install plugin in Jenkins:**
	- Upload the `.hpi` file from `target/` to Jenkins.
7. **Configure plugin:**
	- Set backend URL and API key in Jenkins global configuration.

## API Documentation

### Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
	 "query": "How do I fix npm errors?",
	 "context": {"job_name": "example-job"},
	 "conversation_history": [{"role": "user", "content": "My build failed."}]
  }'
```

### Log Analysis
```bash
curl -X POST http://localhost:8000/api/logs/analyze \
  -H "Content-Type: application/json" \
  -d '{"console_log": "npm ERR! missing package.json"}'
```

### Plugin Recommendation
```bash
curl "http://localhost:8000/api/plugins/recommend?query=docker"
```

### Documentation Search
```bash
curl "http://localhost:8000/api/docs/search?query=pipeline syntax"
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## Configuration Guide
- All API keys and URLs are managed via environment variables in `.env`.
- LLM provider can be switched by setting `LLM_PROVIDER` to `openai`, `gemini`, or `ollama`.
- Jenkins plugin configuration is available in Jenkins global settings.

## Troubleshooting
- **FAISS index missing:** Run `python scripts/index_docs.py` before starting backend.
- **API errors:** Check logs for descriptive error messages.
- **Plugin not visible:** Ensure Jenkins version is 2.387.3+ and plugin is installed.
- **LLM issues:** Verify API keys and provider settings in `.env`.
- **CORS issues:** FastAPI backend includes CORS middleware for plugin communication.
- **Timeouts:** All endpoints are async and respond within 30 seconds.

## Development & Testing
- Unit tests are included for log analyzer, RAG service, and chat endpoint.
- Extend plugin or backend by adding new endpoints or UI features.

---

**Jenkins AI Chatbot is ready for production use!**
# jenkins-doc-chatbot
# ABC Technologies Enterprise AI

An Enterprise AI capstone combining:

- FastAPI backend
- Streamlit dashboard
- Qwen language model
- LangGraph orchestration
- RAG with FAISS
- Customer memory
- MCP business tools
- Human-in-the-loop approval

## Deployment

Backend:
Deploy the backend/ directory as a Render Web Service.

Build command:
pip install -r requirements.txt

Start command:
uvicorn main:app --host 0.0.0.0 --port $PORT

Health check:
/health

Frontend:
Deploy frontend/streamlit_app.py using Streamlit Community Cloud.

Configure API_URL and API_KEY in Streamlit secrets.

IMPORTANT:
The current backend is a deployment scaffold.
The live Qwen, RAG, memory and MCP runtime must be
integrated before full assistant functionality is available.

Never commit API keys or private customer data.

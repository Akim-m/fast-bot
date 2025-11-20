# fast-bot

A lightweight API server built with FastAPI that integrates with Ollama to deliver local large-language-model (LLM) based capabilities.

##  Features  
- REST API service implemented with FastAPI (Python).  
- Uses Ollama as the LLM backend — enabling model inference locally (or self-hosted) for full control.  
- Simple structure: agent + backend modules (see code organisation).  
- Focused on fast, minimal setup for LLM-powered applications.

Right Now the agent can call the weather tool properly and also manage users (create, modify, list and delete)
Also it can hit any endpoint and retrieve the response ( Sometimes it gets out control)

dont change the system prompt much as the tool tends to search the net and fetch details directly without using the weather tool( only for this rn - doesnt help with instructor)

##  Project Structure  
```text
agent/
  └── …                # (contains logic for the “bot”/agent layer)  
backend/
  └── …                # (FastAPI application, endpoints, integration with Ollama)  
.gitattributes


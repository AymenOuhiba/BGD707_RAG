# Configuration centrale
DB_CONFIG = {
    "user": "aymen",
    "password": "aymen",
    "host": "postgres_db",
    "port": "5432",
    "db_name": "rag_db",
    "collection": "rag_knowledge_base",
}

LLM_CONFIG = {
    "url": "http://ollama_server:11434",
    "llm_model": "gemma3:4b",
    "embed_model": "nomic-embed-text:latest",
}

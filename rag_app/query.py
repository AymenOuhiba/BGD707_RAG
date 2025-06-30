import os
from config import DB_CONFIG, LLM_CONFIG
from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


def initialize_components():
    """Initialise les composants Ollama et PostgreSQL"""
    embeddings = OllamaEmbeddings(
        model=LLM_CONFIG["embed_model"], base_url=LLM_CONFIG["url"]
    )

    vector_store = PGVector(
        connection_string=f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db_name']}",
        collection_name=DB_CONFIG["collection"],
        embedding_function=embeddings,
    )
    return vector_store


def setup_rag_chain(vector_store):
    """Configure la chaîne de traitement RAG"""
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    llm = ChatOllama(
        model=LLM_CONFIG["llm_model"],
        base_url=LLM_CONFIG["url"],
        temperature=0.3,  # Ajout pour contrôler la créativité
    )

    prompt = PromptTemplate.from_template(
        """
        SYSTEM: Répondez de manière concise en utilisant uniquement ce contexte:
        {context}

        QUESTION: {question}

        RÉPONSE:
        """
    )

    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def handle_user_interaction(rag_chain):
    """Gère le dialogue avec l'utilisateur"""
    print("Système RAG prêt. Tapez 'exit' ou 'quit' pour quitter.\n")
    while True:
        try:
            query = input("Question: ").strip()
            if query.lower() in ["exit", "quit"]:
                break

            print("\nRéponse:")
            for chunk in rag_chain.stream(query):
                print(chunk, end="", flush=True)
            print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\nInterruption par l'utilisateur")
            break


# Ajoutez cette fonction en haut du fichier query.py
def get_rag_response(question):
    """Nouvelle fonction pour répondre à une question spécifique"""
    vector_store = initialize_components()
    rag_chain = setup_rag_chain(vector_store)

    response = ""
    for chunk in rag_chain.stream(question):
        response += chunk
    return response


def main():
    try:
        # Initialisation
        vector_store = initialize_components()
        rag_chain = setup_rag_chain(vector_store)

        # Interaction utilisateur
        handle_user_interaction(rag_chain)

    except Exception as e:
        print(f"\nErreur critique: {str(e)}")
        print("Vérifiez que les services sont bien démarrés (Ollama, PostgreSQL)")


if __name__ == "__main__":
    main()

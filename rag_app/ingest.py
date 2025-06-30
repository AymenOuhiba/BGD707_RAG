import os
import warnings
from config import DB_CONFIG, LLM_CONFIG
from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

# Désactive les avertissements pandas
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")


def load_and_chunk_data():
    """Charge et découpe les documents"""
    loader = HuggingFaceDatasetLoader("neural-bridge/rag-dataset-12000", "context")
    documents = list(loader.load())[:100]  # Limite à 100 documents

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)


def init_embeddings():
    """Initialise le modèle d'embedding"""
    return OllamaEmbeddings(model=LLM_CONFIG["embed_model"], base_url=LLM_CONFIG["url"])


def store_in_postgres(chunks, embeddings):
    """Stocke les données vectorisées dans PostgreSQL"""
    PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        collection_name=DB_CONFIG["collection"],
        connection_string=f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db_name']}",
        pre_delete_collection=True,
    )


def main():
    try:
        print("Début de l'ingestion des données...")

        # 1. Chargement et découpage
        chunks = load_and_chunk_data()
        print(f"{len(chunks)} chunks créés")
        print("\nGénération des embeddings...")
        print("Patientez, cette opération peut être longue.")
        # 2. Initialisation des embeddings
        embeddings = init_embeddings()

        # 3. Stockage dans PostgreSQL
        store_in_postgres(chunks, embeddings)
        print("Base de connaissances créée avec succès")

    except Exception as e:
        print(f"Erreur lors de l'ingestion: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()

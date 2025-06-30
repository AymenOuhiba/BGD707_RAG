# rag-llm-local

Ce projet propose une implémentation locale d’un système RAG (Retrieval-Augmented Generation) en combinant Ollama pour les modèles de langage et PostgreSQL avec l’extension pgvector pour la gestion des vecteurs. Il permet l’ingestion de documents, la recherche contextuelle et la génération de réponses enrichies. L’ensemble est entièrement orchestré via Docker Compose. Idéal pour tester une architecture RAG en local avec vos propres données.

## Exécution du projet

```bash
# Cloner le dépôt
git clone https://github.com/audedef/rag-llm-local.git
cd rag-llm-local

# Ajouter vos fichiers dans le dossier : rag_app/knowledge_base/

# Démarrer les services
docker-compose up --build -d

# Télécharger les modèles nécessaires (si ce n'est pas déjà fait)
docker exec -it ollama_server ollama run gemma3:4b
docker exec -it ollama_server ollama pull nomic-embed-text

# Vérifier les modèles présents
docker exec -it ollama_server ollama list

# Ingérer les documents
docker compose exec rag-app python ingest.py

# Lancer les requêtes
docker compose exec rag-app python query.py
```

## Évaluation du système

Un script est disponible pour tester automatiquement la qualité des réponses générées à partir de questions prédéfinies.

```bash
docker compose exec rag-app python evaluate.py
```

Les résultats seront affichés sous forme de tableau dans le terminal et enregistrés dans evaluation_results.md.

import time
import pandas as pd
from config import DB_CONFIG, LLM_CONFIG
from query import main as query_system
from query import get_rag_response

QUESTIONS = [
    {
        "type": "Dans la base",
        "question": "Advise me some podcasts about love and relationships",
    },
    {
        "type": "Dans la base",
        "question": "Why is concrete recycling important in construction?",
    },
    {
        "type": "Dans la base",
        "question": "Who has the most Instagram followers currently?",
    },
    {
        "type": "Sujet proche",
        "question": "What are the best relationship advice books?",
    },
    {
        "type": "Sujet proche",
        "question": "How does concrete recycling work technically?",
    },
    {"type": "Hors base", "question": "Who was the first US President?"},
    {"type": "Hors base", "question": "Explain quantum computing basics"},
    {"type": "Créatif", "question": "Write a short poem about AI"},
    {"type": "Test limite", "question": "Convertis 100 euros en dollars canadien"},
]


def main():
    results = []
    for q in QUESTIONS:
        start = time.time()
        response = get_rag_response(q["question"])  # Changé ici
        results.append(
            {
                "Type": q["type"],
                "Question": q["question"],
                "Réponse": response,
                "Temps (s)": f"{time.time() - start:.2f}",
            }
        )

    df = pd.DataFrame(results)
    print(df.to_markdown(index=False))

    with open("evaluation_results.md", "w") as f:
        f.write("# Résultats d'évaluation RAG\n\n")
        f.write(df.to_markdown(index=False))


if __name__ == "__main__":
    main()

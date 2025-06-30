# Utilisation d'une image Python officielle légère
FROM python:3.10-slim-bookworm

# Définition des variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Configuration du répertoire de travail
WORKDIR /app

# Copie des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie de l'ensemble du code applicatif
COPY . .

# Commande de maintien du conteneur actif
CMD ["tail", "-f", "/dev/null"]
#!/bin/bash
# build_files.sh
echo "BUILD START"

# Installer les dépendances Python
python -m pip install -r requirements.txt

# Créer les migrations si nécessaire
python manage.py makemigrations --noinput || echo "No new migrations"

# Appliquer les migrations
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput --clear

echo "BUILD END"

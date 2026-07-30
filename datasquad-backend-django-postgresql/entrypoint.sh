#!/bin/sh
set -e

echo "→ Application des migrations..."
python manage.py migrate --noinput

echo "→ Vérification du compte admin..."
python manage.py ensure_admin

echo "→ Démarrage du serveur..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}

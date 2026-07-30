FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

# collectstatic n'a pas besoin de la base de données, on peut le faire au build
RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput --settings=config.settings || true

EXPOSE 8000
CMD ["./entrypoint.sh"]

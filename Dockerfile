FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=projeto_arq.settings

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "projeto_arq.wsgi:application"]
# Usar uma imagem Python oficial estável
FROM python:3.11-slim

# Evitar a geração de arquivos .pyc e garantir que logs apareçam no console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema para o Postgres (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas os requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . /app/

# Criar diretório para arquivos estáticos
RUN mkdir -p /app/staticfiles

# Porta padrão (pode ser sobrescrita via env)
ENV PORT=8000
EXPOSE 8000

# Script de entrada para garantir que o banco esteja pronto (opcional mas recomendado)
# Por ora, rodar o waitress diretamente. O docker-compose cuidará da dependência.
CMD ["python", "run_waitress.py"]

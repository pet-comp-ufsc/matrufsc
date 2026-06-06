# Usando a versão slim para manter a imagem leve
FROM python:3.12-trixie

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Sao_Paulo

WORKDIR /app

# Instalando dependências do sistema para o fuso horário e limpeza
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Instalando dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código da aplicação
COPY ./app ./app

# Criando a pasta de dados onde os JSONs serão persistidos
RUN mkdir -p /app/data

# Expondo a porta padrão do FastAPI
EXPOSE 8000

# Comando para rodar a API usando o Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
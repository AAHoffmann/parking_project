# 1. Imagem base: Começamos com uma imagem oficial do Python.
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do contêiner.
WORKDIR /code

# 3. Copia o arquivo de dependências e instala as bibliotecas.
# Copiamos este arquivo primeiro para aproveitar o cache do Docker.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Copia o resto do código da nossa aplicação para o contêiner.
COPY ./app /code/app

# 5. Comando para executar a aplicação quando o contêiner iniciar.
# O host 0.0.0.0 é essencial para que a aplicação seja acessível de fora do contêiner.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
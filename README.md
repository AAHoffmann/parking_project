Documento 1: Manual de Execução do Projeto (com Docker Compose)
Manual de Execução: Sistema de Gerenciamento de Estacionamento com Docker Compose
1. Visão Geral
Este manual fornece as instruções para configurar e executar a aplicação de gerenciamento de estacionamento em um ambiente local utilizando Docker e Docker Compose. A aplicação é composta por múltiplos microsserviços containerizados que são orquestrados para funcionar de forma integrada.

2. Pré-requisitos
Antes de começar, garanta que os seguintes softwares estão instalados e configurados em sua máquina:

Git: Para clonar o repositório do projeto.
Docker Desktop: Inclui o Docker Engine e o Docker Compose, essenciais para rodar a aplicação.
(Opcional, mas recomendado) MongoDB Compass: Para visualizar os dados persistidos no banco de dados.
(Opcional) Um editor de código como o VS Code.
3. Configuração e Execução
Clonar o Repositório:
Bash

# Use o comando para o repositório real do projeto
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
Iniciar a Aplicação: Com o Docker Desktop em execução, abra um terminal na pasta raiz do projeto e execute o seguinte comando:
Bash

docker-compose up --build
O que este comando faz?
--build: Constrói as imagens Docker para os serviços api e worker a partir de seus Dockerfile.
up: Cria uma rede virtual para os serviços e inicia um contêiner para cada serviço definido no arquivo docker-compose.yml (api, worker, redis, rabbitmq, mongo).
O terminal exibirá os logs de todos os serviços em tempo real.
4. Verificação e Acesso
Após a execução do comando, os serviços estarão disponíveis nos seguintes endereços na sua máquina local (localhost):

Acessar a Interface Web da Aplicação:

Abra seu navegador e acesse: http://localhost:8000
Acessar a Interface de Gerenciamento do RabbitMQ:

Para visualizar as filas e mensagens em trânsito.
Acesse: http://localhost:15672
Login: guest / Senha: guest
Verificar os Dados no MongoDB:

Abra o MongoDB Compass.
Crie uma nova conexão utilizando a seguinte string (URI):
mongodb://mongoadmin:secret@localhost:27017/
Clique em "Connect". Você poderá navegar pelo banco de dados parking_db e ver os registros na coleção parking_history.

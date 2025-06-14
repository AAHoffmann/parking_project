🚗 Sistema de Gerenciamento de Estacionamento Distribuído
Este repositório contém o código-fonte de um sistema de gerenciamento de estacionamento desenvolvido com uma arquitetura de microsserviços, orientado a eventos e orquestrado localmente com Docker Compose.

📜 Visão Geral
O projeto demonstra a aplicação de padrões de arquitetura distribuída em um caso de uso prático. A aplicação é composta por múltiplos serviços independentes e containerizados que se comunicam de forma assíncrona, garantindo resiliência e escalabilidade.

Arquitetura: Microsserviços, Orientada a Eventos (EDA), Persistência Poliglota.
Tecnologias: Python (FastAPI), Docker, Docker Compose, RabbitMQ, Redis, MongoDB.
🛠️ Pré-requisitos
Antes de começar, garanta que os seguintes softwares estão instalados e configurados em sua máquina:

Git
Docker Desktop (inclui Docker e Docker Compose)
(Opcional) MongoDB Compass para visualizar os dados.
🚀 Configuração e Execução
Siga os passos abaixo para clonar o repositório e iniciar a aplicação completa.

1. Clone o Repositório

Bash

# Clone este repositório para a sua máquina local
git clone <URL_DO_SEU_REPOSITORIO>

# Navegue até a pasta do projeto
cd <NOME_DA_PASTA_DO_PROJETO>
2. Inicie a Aplicação com Docker Compose

Com o Docker Desktop em execução, execute o seguinte comando no terminal, na pasta raiz do projeto.

Bash

docker-compose up --build
--build: Garante que as imagens Docker para os serviços api e worker sejam construídas a partir dos Dockerfile.
up: Inicia todos os serviços (api, worker, redis, rabbitmq, mongo), redes e volumes definidos no arquivo docker-compose.yml.
O terminal exibirá os logs de todos os serviços em tempo real. Aguarde até que as mensagens de inicialização apareçam para todos os contêineres.

✅ Verificação e Acesso
Após a inicialização completa, os serviços estarão acessíveis nos seguintes endereços:

🌐 Aplicação Web Principal
URL: http://localhost:8000
Descrição: Interface principal para realizar o check-in e check-out de veículos.
🐰 RabbitMQ Management UI
URL: http://localhost:15672
Descrição: Interface para monitorar o status do RabbitMQ, visualizar filas e mensagens.
Login: guest
Senha: guest
🍃 Banco de Dados MongoDB
Ferramenta: Use o MongoDB Compass para se conectar.
String de Conexão:
mongodb://mongoadmin:secret@localhost:27017/
Descrição: Após conectar, você poderá ver o banco de dados parking_db e a coleção parking_history com os registros de todos os check-outs processados.
⚙️ Comandos Úteis do Docker Compose
Iniciar serviços em segundo plano (detached mode):
Bash

docker-compose up -d
Ver o status dos serviços em execução:
Bash

docker-compose ps
Acompanhar os logs de um serviço específico (ex: worker):
Bash

docker-compose logs -f worker
Parar e remover contêineres e redes:
Bash

docker-compose down
🧹 Limpando o Ambiente
Para parar completamente a aplicação e remover todos os dados persistidos nos volumes (útil para começar do zero), use o comando:

Bash

docker-compose down -v
A flag -v remove os volumes nomeados, limpando os bancos de dados.

import datetime
import os
import redis
import pika
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Cria a aplicação FastAPI
app = FastAPI(title="Parking Management System")

# Configura o diretório de templates
templates = Jinja2Templates(directory="app/templates")

# --- Conexão com o Redis ---
# Pega o nome do host do Redis da variável de ambiente que definimos no docker-compose.
# Se não encontrar, usa 'localhost' (útil para rodar localmente sem Docker).
redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True) # decode_responses=True para receber strings em vez de bytes

# --- Endpoints da Interface Web e API ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Exibe a página principal com a lista de carros estacionados lendo do Redis.
    """
    parked_cars = {}
    # Busca todas as chaves que seguem o padrão "car:*"
    car_keys = r.keys("car:*")
    for key in car_keys:
        # Para cada chave, busca os dados (hash) do carro
        plate = key.split(":")[1]
        parked_cars[plate] = r.hgetall(key)

    # Ordena os carros pela hora de entrada
    sorted_cars = sorted(parked_cars.items(), key=lambda item: item[1]['entry_time'])
    return templates.TemplateResponse(
        "index.html", {"request": request, "parked_cars": dict(sorted_cars)}
    )

@app.post("/check-in")
async def check_in(plate: str = Form(...)):
    """
    Registra a entrada de um novo carro no Redis.
    """
    if not r.exists(f"car:{plate}"):
        now = datetime.datetime.now(datetime.timezone.utc)
        # Usamos um Hash no Redis para armazenar os dados do carro.
        # Isso é mais flexível para adicionar mais campos no futuro.
        r.hset(f"car:{plate}", mapping={
            "entry_time": now.isoformat()
        })
    
    return RedirectResponse(url="/", status_code=303)

# --- Conexão com RabbitMQ para a API ---
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='checkout_queue', durable=True)

@app.post("/check-out")
async def check_out(plate: str = Form(...)):
    """
    APENAS publica uma mensagem no RabbitMQ para processamento assíncrono.
    Não faz mais nenhuma lógica de negócio.
    """
    channel.basic_publish(
        exchange='',
        routing_key='checkout_queue', # O nome da fila
        body=plate.encode(), # O corpo da mensagem (a placa)
        properties=pika.BasicProperties(
            delivery_mode=2,  # Torna a mensagem persistente
        ))
    
    print(f"API sent message to checkout car: {plate}")
    
    # A resposta é imediata, não esperamos o processamento.
    return RedirectResponse(url="/", status_code=303)
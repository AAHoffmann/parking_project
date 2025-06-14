import pika
import os
import time
import redis
import json
from datetime import datetime
from pymongo import MongoClient

print('⏳ Worker starting...')
time.sleep(15) # Aumentamos o tempo para garantir que todos os serviços (especialmente o mongo) estejam prontos

# --- Conexões ---

# RabbitMQ
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue='checkout_queue', durable=True)

# Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# MongoDB
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_user = os.getenv('MONGO_USER', 'mongoadmin')
mongo_pass = os.getenv('MONGO_PASS', 'secret')
mongo_client = MongoClient(f'mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017/')
db = mongo_client.parking_db # Nome do nosso banco de dados
parking_history_collection = db.parking_history # Nome da nossa "tabela" (collection)

print('✅ Worker connected to RabbitMQ, Redis, and MongoDB. Waiting for messages.')

# --- Lógica de Processamento ---

def process_checkout(ch, method, properties, body):
    plate = body.decode()
    print(f"Received message to checkout car: {plate}")

    car_data = r.hgetall(f"car:{plate}")
    if not car_data:
        print(f"Car {plate} not found in Redis. Acknowledging message.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Calcula duração e preço
    entry_time_str = car_data.get('entry_time')
    entry_time = datetime.fromisoformat(entry_time_str)
    exit_time = datetime.now(entry_time.tzinfo)
    duration = exit_time - entry_time
    duration_minutes = duration.total_seconds() / 60
    price = duration_minutes * 0.15

    # Cria o documento para salvar no MongoDB
    parking_record = {
        "plate": plate,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "duration_minutes": round(duration_minutes, 2),
        "price": round(price, 2)
    }

    # Salva o registro no MongoDB
    try:
        parking_history_collection.insert_one(parking_record)
        print(f"✅ Record for {plate} saved to MongoDB.")
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")

    # Remove o carro do Redis (estado em tempo real)
    r.delete(f"car:{plate}")
    
    # Confirma que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("---------------------------------")


# --- Consumidor ---
channel.basic_consume(queue='checkout_queue', on_message_callback=process_checkout)
channel.start_consuming()
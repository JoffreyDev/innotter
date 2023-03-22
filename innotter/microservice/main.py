from fastapi import FastAPI
import pika
import json

app = FastAPI()

@app.get("/statistics/{user_id}")
async def get_user_statistics(user_id: int):
    # Получаем данные из базы данных и формируем статистику
    # ...

    # Подготавливаем ответ
    response = {
        'user_id': user_id,
        'statistics': statistics,
    }

    # Отправляем ответ на очередь RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='user_statistics', body=json.dumps(response))
    connection.close()

    # Возвращаем ответ пользователю
    return response

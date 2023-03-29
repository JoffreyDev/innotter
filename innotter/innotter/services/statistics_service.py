import pika
from innotter.settings import rabbitmq_user, rabbitmq_password, rabbitmq_host, rabbitmq_port, rabbitmq_virtual_host
import requests

def send_user_id_to_rabbitmq(sender, instance, **kwargs):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, rabbitmq_virtual_host, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='statistics')
    channel.basic_publish(exchange='', routing_key='statistics', body=str(instance.id))
    connection.close()

def get_user_statistics_from_microservice(user_id):
    response = requests.get(f'https://microservice:8001/{user_id}')
    return response.json()

    
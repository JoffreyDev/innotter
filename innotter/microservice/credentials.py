import psycopg2
from dotenv import load_dotenv
import os
from os.path import join, dirname
import boto3
import pika

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
load_dotenv('.env')

# PSQL настройки


def connect_to_db():
    conn = psycopg2.connect(
        host='db',
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn


# RabbitMQ настройки
def get_rabbitmq_creds():
    rabbitmq_host = "rabbitmq"
    rabbitmq_virtual_host = '/'
    rabbitmq_port = 5672
    rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER')
    rabbitmq_password = os.environ.get('RABBITMQ_DEFAULT_PASS')
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(
        rabbitmq_host, rabbitmq_port, rabbitmq_virtual_host, credentials)
    return parameters


# AWS настройки
AWS_REGION_NAME = 'us-east-2'
dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIATL2UT275A33NU3XI',
                          aws_secret_access_key='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', region_name=AWS_REGION_NAME)
table_name = 'innotter-db'
table = dynamodb.Table(table_name)

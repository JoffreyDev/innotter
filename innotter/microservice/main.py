from fastapi import FastAPI
import pika
from .credentials import connect_to_db, get_rabbitmq_creds, table

app = FastAPI()

# SQL-запрос для получения статистики из PostgreSQL
sql = """
SELECT
    (SELECT COUNT(*) FROM entities_post WHERE page_id IN
        (SELECT id FROM entities_page WHERE owner_id = %s)) AS num_posts,
    (SELECT COUNT(*) FROM entities_post_likes WHERE post_id IN
        (SELECT id FROM entities_post WHERE page_id IN
            (SELECT id FROM entities_page WHERE owner_id = %s))) AS num_likes,
    (SELECT COUNT(*) FROM entities_page_followers WHERE page_id IN
        (SELECT id FROM entities_page WHERE owner_id = %s)) AS num_followers;
"""


@app.on_event('startup')
def startup_event():
    connection = pika.BlockingConnection(get_rabbitmq_creds())
    channel = connection.channel()
    channel.queue_declare(queue='statistics')
    channel.basic_consume(queue='statistics',
                          on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def callback(ch, method, properties, body):
    user_id = int(body)
    get_statistics(user_id)


# Получение статистики из PostgreSQL
def get_statistics(user_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(sql, (user_id, user_id, user_id))
    result = cur.fetchall()
    if check_if_user_exists(user_id):
        update_statistics_in_dynamodb(user_id, result)
    else:
        write_statistics_to_dynamodb(user_id, result)

    cur.close()
    conn.close()

# Проверка существования записи о пользователе
def check_if_user_exists(user_id):
    try:
        table.get_item(Key={'user': str(user_id)})
        return True
    except:
        return False


# Запись статистики в AWS DynamoDB
def write_statistics_to_dynamodb(user, data):
    table.put_item(Item={'user': str(user), 'posts': data[0][0], 'likes': data[0][1], 'followers': data[0][2]})


# Апдейт статистки в AWS DynamoDB
def update_statistics_in_dynamodb(user, data):
    response = table.update_item(
                Key={'user': str(user)},
                UpdateExpression="set posts=:p, likes=:l, followers=:f",
                ExpressionAttributeValues={
                    ':p': data[0][0], ':l': data[0][1], ':f': data[0][2]},
                ReturnValues="UPDATED_NEW")
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Эндпоинт для получения статистики по запросу
@app.get('/{user_id}')
async def get_users(user_id: int):
    try:
        response = table.get_item(Key={'user': str(user_id)})
        return response
    except:
        return 'no data found'

from celery import Celery

app = Celery('innotter', broker='pyamqp://admin@localhost//', backend='rpc://')

app.conf.task_routes = {
    'myapp.tasks.*': {'queue': 'mail'},
}
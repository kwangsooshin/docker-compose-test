import os
from celery import Celery
from celery.schedules import crontab
from AnalysisSite import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnalysisSite.settings')

app = Celery('AnalysisSite')

if 'RABBITMQ_DEFAULT_USER' in os.environ:
    url = 'amqp://{}:{}@{}'.format(
                                os.environ['RABBITMQ_DEFAULT_USER'],
                                os.environ['RABBITMQ_DEFAULT_PASS'],
                                os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', 'rabbitmq'))
else:
    url = 'amqp://localhost',

print(url)

app.conf.update(
    broker_url=url,
    result_backend='amqp://localhost',
    timezone='UTC',
    enable_utc=True,
    worker_autoscaler='{0},{1}'.format(config.WORKER_MAX_SCALER, config.WORKER_MIN_SCALER),
    worker_concurrency='{0}'.format(config.WORKER_CONCURRENCY),
)

app.autodiscover_tasks()
app.autodiscover_tasks(related_name='beats')

app.conf.beat_schedule = {
    'delete-old-database': {
        'task': 'ModuleCommunicator.beats.delete_old_database',
        'schedule': crontab(
            hour=config.DATABASE_AUTO_DELETE_HOUR,
            minute=config.DATABASE_AUTO_DELETE_MINUTE,
            day_of_week=config.DATABASE_AUTO_DELETE_DAY_OF_WEEK,
        ),
        'args': (config.DATABASE_AUTO_DELETE_BEFORE_DAYS, ),
    },
}

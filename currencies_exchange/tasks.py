from celery import Celery
import config
import logging
import currencies_parser

logger = logging.getLogger(__name__)

app = Celery('tasks', broker=config.RABBITMQ_HOST)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    print("Task configure")
    sender.add_periodic_task(3600.0, get_currencies.s(), name='Get currencies')


@app.task
def get_currencies():
    logger.debug("Get currencies task")
    currencies_parser.get_currencies()

import logging

PORT = 9003

DATA_PATH = '/Users/vitaliykrasnov/Desktop/'

# Logging
LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_FILE = None

RABBITMQ_HOST = "pyamqp://celery:celery@51.15.40.35//"
import logging
import config
import aiohttp_jinja2
import jinja2
from aiohttp import web

from router import routes

logging.basicConfig(filename=config.LOG_FILE, filemode='w', level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)

logger.info('Configuring restricted urls')
restricted_rules = []
logger.debug('Restricted urls configure: {}'.format(restricted_rules))

app = web.Application()
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('./templates'))
app.add_routes(routes)

logger.info('Starting app...')
web.run_app(app, port=config.PORT)

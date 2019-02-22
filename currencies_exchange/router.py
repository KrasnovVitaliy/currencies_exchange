from aiohttp import web
from views import *

# Define all routes and views here

# path_to_static_folder = './data'
routes = [
    web.view('/', IndexView),
]

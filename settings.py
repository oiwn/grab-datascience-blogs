import os
import sys
import logging

from pymongo import MongoClient

DEBUG = True
# set DEBUG value from os environment
if 'DEBUG' in os.environ:
    if os.environ['DEBUG'] == 'true':
        DEBUG = True
    elif os.environ['DEBUG'] == 'false':
        DEBUG = False

if DEBUG is True:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

DB_NAME = 'grabdatascienceblogs'
# http://docs.mongodb.org/manual/reference/connection-string/
DB_URI = 'mongodb://localhost:27017/{}'.format(DB_NAME)
if 'MONGO_URI' in os.environ:
    DB_URI = os.environ['MONGO_URI']

SPIDER_CONFIG = {
    'thread_number': 20,
    'network_try_limit': 3,
    'task_try_limit': 3,
    'max_task_generator_chunk': 5,
    'priority_mode': 'const',
    # 'mp_mode': True,  # won't work under python 2.7
    # 'parser_pool_size': 3,
}

BLOGS_LIST = ('https://raw.githubusercontent.com/rushter'
              '/data-science-blogs/master/data-science.opml')


def db_connection():
    client = MongoClient(DB_URI.format(''))
    return client[DB_NAME]

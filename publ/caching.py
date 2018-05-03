# caching.py
""" Useful caching functions """

from flask_caching import Cache
from flask import request

from . import config

cache = Cache()


def init_app(app):
    cache.init_app(app, config=config.cache)


def make_category_key():
    """ Key generator for categories """
    return 'category/' + request.full_path


def make_entry_key():
    """ Key generator for entries """
    return 'entry/' + request.path
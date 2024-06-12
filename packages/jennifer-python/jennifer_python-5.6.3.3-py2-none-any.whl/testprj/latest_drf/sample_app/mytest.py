
import types
from html import escape
import os
from distutils.version import LooseVersion


# http://192.168.0.8:18008/unit_test
def all_test():
    result_txt = ""
    print(os.getpid(), '[jennifer]', 'info', 'all_test')

    result_txt += check_intercept()
    return result_txt


def check_intercept():
    import sys

    result = ""

    must_be = [
        # ('jennifer.wrap.wsgi', check_wsgi),
        # not installed ('jennifer.hooks.app_flask', None),
        ('jennifer.hooks.db_sqlite3', check_sqlite3),
        ('jennifer.hooks.app_django', check_django),
        ('jennifer.hooks.db_mysqlclient', check_mysqlclient),
        ('jennifer.hooks.db_pymysql', check_pymysql),
        ('jennifer.hooks.external_requests', check_requests),
        ('jennifer.hooks.external_urllib', check_urllib),
        ('jennifer.hooks.external_urllib3', check_urllib3),
        # ('jennifer.api.proxy', None),
        ('jennifer.hooks.db_pymongo', check_pymongo),
        ('jennifer.hooks.db_redis', check_redis),
        ('jennifer.hooks.db_cx_oracle', check_cx_oracle),
        ('jennifer.hooks.db_psycopg2', check_psycopg2),
        ('jennifer.hooks', check_builtins),
    ]

    for module in must_be:
        if module[0] not in sys.modules.keys():
            result += "EXCEPTION: NO JENNIFER MODULE: " + module[0] + "<br />\n"
        else:
            target_module = __import__(module[0])
            result += "info: " + module[0] + " imported: " + target_module.__package__ + "<br />\n"

            func = module[1]
            if func is not None:
                result += module[1](target_module)

    result += test_info()

    for key in sys.modules.keys():
        # result += "info: " + key + ", " + "<br />\n"
        pass

    return result


def test_info():
    text = ""

    try:
        text = "info: " + str(os.getpid()) + ' ' + os.environ['DIR_ROOT'] + "<br />\n"
    except Exception as e:
        text = "info: " + str(os.getpid()) + " local_test<br />\n"

    return text


def check_builtins(module):
    import socket

    check_funcs = [
        (__builtins__['open'], "_wrap_file_open.<locals>._handler"),
        (socket.socket.connect, "_wrap_socket_connect.<locals>._handler"),
        (socket.socket.connect_ex, "_wrap_socket_connect.<locals>._handler"),
    ]

    return check_funcs_all(check_funcs)


def check_sqlite3(module):
    import sqlite3

    check_funcs = [
        (sqlite3.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
        (sqlite3.dbapi2.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_cx_oracle(module):
    import cx_Oracle

    check_funcs = [
        (cx_Oracle.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_redis(module):
    import redis

    check_funcs = [
        (redis.Redis.execute_command, "wrap_execute_command.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_django(module):
    from django.core.handlers.wsgi import WSGIHandler
    from django.core.handlers.asgi import ASGIHandler

    check_funcs = [
        (WSGIHandler.__call__, "_wrap_wsgi_handler.<locals>.handler"),
        (ASGIHandler.__call__, "wrap_django_asgi_handler.<locals>._handler"),
    ]

    result = ""
    for func_item in check_funcs:
        result += func_name_check(func_item[0], func_item[1]) + "<br />\n"

    return result


def check_pymongo(module):
    import pymongo

    current_ver = LooseVersion(pymongo.__version__)
    base_ver = LooseVersion("3.12.3")
    check_funcs = None

    if current_ver <= base_ver:
        check_funcs = [
            (pymongo.MongoClient, "hook.<locals>.MongoClientWrap3"),
        ]
    else:
        check_funcs = [
            (pymongo.MongoClient, "hook.<locals>.MongoClientWrap4"),
        ]

    return check_funcs_all(check_funcs)


def check_urllib(module):
    import urllib

    check_funcs = [
        (urllib.request.urlopen, "wrap_urlopen.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_urllib3(module):
    import urllib3

    check_funcs = [
        (urllib3.poolmanager.PoolManager.request, "wrap_request.<locals>.handler"),
        (urllib3.poolmanager.PoolManager.urlopen, "wrap_request.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_requests(module):
    import requests

    check_funcs = [
        (requests.Session.send, "wrap_send.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_pymysql(moulde):
    import pymysql

    check_funcs = [
        (pymysql.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_mysqlclient(module):
    import MySQLdb

    check_funcs = [
        (MySQLdb.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
    ]

    return check_funcs_all(check_funcs)


def check_psycopg2(module):
    import psycopg2

    check_funcs = [
        (psycopg2.connect, "register_database.<locals>._wrap_connect.<locals>.handler"),
        (psycopg2.extensions.register_type, "_wrap_register_type.<locals>.handler"),
        (psycopg2._psycopg.register_type, "_wrap_register_type.<locals>.handler"),
        (psycopg2._json.register_type, "_wrap_register_type.<locals>.handler"),
    ]

    result = ""
    for func_item in check_funcs:
        result += func_name_check(func_item[0], func_item[1]) + "<br />\n"

    return result


def func_name_check(func, func_name):
    if func.__qualname__ == func_name:
        return "info: Intercepted: " + escape(func_name, "<")

    return "exception: NOT INTERCEPTED: " + escape(func_name, "<") + ", " + escape(func.__qualname__, "<")


def check_funcs_all(check_funcs):

    result = ""
    for func_item in check_funcs:
        result += func_name_check(func_item[0], func_item[1]) + "<br />\n"

    return result

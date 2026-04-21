from django.shortcuts import render
from django.db import connection
from django.conf import settings

import psycopg2
from psycopg2 import Error

# Create your views here.
def init(request):
    message = "OK"
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex00_movies (
                           title            VARCHAR(64) UNIQUE NOT NULL,
                           episode_nb       INTEGER PRIMARY KEY,
                           opening_crawl    TEXT,
                           director         VARCHAR(32) NOT NULL,
                           producer         VARCHAR(128) NOT NULL,
                           release_date     DATE NOT NULL
                           );
                """)
    except Error as e:
        message = str(e)
    return render(request, "ex00/init.html", {"message": message})

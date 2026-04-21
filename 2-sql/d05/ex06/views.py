from django.shortcuts import render
from django.db import connection
from django.conf import settings
from datetime import date

# Create your views here.
def init(request):
    message = "OK"
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex06_movies (
                           title            VARCHAR(64) UNIQUE NOT NULL,
                           episode_nb       INTEGER PRIMARY KEY,
                           opening_crawl    TEXT,
                           director         VARCHAR(32) NOT NULL,
                           producer         VARCHAR(128) NOT NULL,
                           release_date     DATE NOT NULL,
                           created          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           );

                CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                RETURNS TRIGGER AS $$
                BEGIN
                NEW.updated = now();
                NEW.created = OLD.created;
                RETURN NEW;
                END;
                $$ language 'plpgsql';
                CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                update_changetimestamp_column();
                """)
    except Exception as e:
        message = str(e)
    return render(request, "ex06/init.html", {"message": message})

def populate(request):
    movies = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": date(1999, 5, 19),
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": date(2002, 5, 16),
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": date(2005, 5, 19),
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": date(1977, 5, 25),
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": date(1980, 5, 17),
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": date(1983, 5, 25),
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J.J.Abrams, Bryan Burk",
            "release_date": date(2015, 12, 11),
        },
    ]

    messages = []
    for movie in movies:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO ex06_movies (title, episode_nb, opening_crawl, director, producer, release_date)
                    VALUES ( 
                               '{movie.get("title", "")}',
                               {movie.get("episode_nb")},
                               '{movie.get("opening_crawl", "")}',
                               '{movie.get("director", "")}',
                               '{movie.get("producer", "")}',
                               '{movie.get("release_date", "")}'
                               );
                    """)
            messages.append(f"OK : {movie["title"]}")
        except Exception as e:
            messages.append(f"Fail : {movie["title"]}; Reason : {str(e)}")
    return render(request, "ex06/populate.html", {"messages": messages})

def display(request):
    movies = get_movies()
    return render(request, "ex06/display.html", {"movies": movies})

def remove(request):
    if request.method == "POST":
        id = request.POST.get("to_remove")
        if id:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    DELETE FROM ex06_movies
                    WHERE episode_nb = {id};
                    """)
    movies = get_movies()
    return render(request, "ex06/remove.html", {"movies": movies})

def update(request):
    if request.method == "POST":
        id = request.POST.get("to_update")
        if id:
            opening = request.POST.get("opening")
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE ex06_movies
                    SET opening_crawl = '{opening}'
                    WHERE episode_nb = {id};
                    """)
    movies = get_movies()
    return render(request, "ex06/update.html", {"movies": movies})

def get_movies():
    #Throws when table does not exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT title, episode_nb, opening_crawl, director, producer, release_date, created, updated
            FROM ex06_movies
            ORDER BY episode_nb;
            """)
        data = cursor.fetchall()
        movies = []
        for item in data:
            movies.append({
                "title": item[0],
                "episode_nb": item[1],
                "opening_crawl": item[2],
                "director": item[3],
                "producer": item[4],
                "release_date": item[5],
                "created": item[6],
                "updated": item[7],
            })
    return movies

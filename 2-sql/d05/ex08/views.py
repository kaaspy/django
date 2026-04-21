from django.shortcuts import render
from django.db import connection
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from io import StringIO

# Create your views here.
def init(request):
    message = "OK"
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex08_planets (
                           id               SERIAL PRIMARY KEY,
                           name             VARCHAR(64) UNIQUE NOT NULL,
                           climate          TEXT,
                           diameter         INTEGER,
                           orbital_period   INTEGER,
                           population       BIGINT,
                           rotation_period  INTEGER,
                           surface_water    REAL,
                           terrain          VARCHAR(128)
                           );

                CREATE TABLE IF NOT EXISTS ex08_people (
                           id               SERIAL PRIMARY KEY,
                           name             VARCHAR(64) UNIQUE NOT NULL,
                           birth_year       VARCHAR(32),
                           gender           VARCHAR(32),
                           eye_color        VARCHAR(32),
                           hair_color       VARCHAR(32),
                           height           INTEGER,
                           mass             REAL,
                           homeworld        VARCHAR(64),

                           CONSTRAINT fk_people_homeworld
                           FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
                           );

                """)
    except Exception as e:
        message = str(e)
    return render(request, "ex08/init.html", {"message": message})

def populate(request):
    messages = []
    #Must run a collectstatic to work in prod (production standard practice)
    with open(staticfiles_storage.path("csv/planets.csv"), "r") as f:
        io = StringIO(f.read())
        try:
            with connection.cursor() as cursor:
                cursor.copy_from(
                    file=io,
                    table="ex08_planets",
                    sep="\t",
                    null="NULL",
                    columns=[
                        "name",
                        "climate",
                        "diameter",
                        "orbital_period",
                        "population",
                        "rotation_period",
                        "surface_water",
                        "terrain",
                    ]
                )
            messages.append(f"OK : planets.csv")
        except Exception as e:
            messages.append(f"Fail : planets.csv; Reason : {str(e)}")
            
    #Must run a collectstatic to work in prod (production standard practice)
    with open(staticfiles_storage.path("csv/people.csv"), "r") as f:
        io = StringIO(f.read())
        try:
            with connection.cursor() as cursor:
                cursor.copy_from(
                    file=io,
                    table="ex08_people",
                    sep="\t",
                    null="NULL",
                    columns=[
                        "name",
                        "birth_year",
                        "gender",
                        "eye_color",
                        "hair_color",
                        "height",
                        "mass",
                        "homeworld",
                    ]
                )
            messages.append(f"OK : people.csv")
        except Exception as e:
            messages.append(f"Fail : people.csv; Reason : {str(e)}")
    return render(request, "ex08/populate.html", {"messages": messages})

def display(request):
    #Throws when table does not exists
    with connection.cursor() as cursor:
        #Left join to allow every character to be displayed
        cursor.execute("""
            SELECT ppl.name, ppl.homeworld, plt.climate
            FROM ex08_people AS ppl
            LEFT JOIN ex08_planets AS plt 
                ON ppl.homeworld = plt.name
            WHERE plt.climate LIKE '%windy%'
            ORDER BY ppl.name;
            """)
        data = cursor.fetchall()
        people = []
        for item in data:
            people.append({
                "name": item[0],
                "homeworld": item[1],
                "climate": item[2],
            })
    return render(request, "ex08/display.html", {"people": people})

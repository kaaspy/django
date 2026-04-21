from django.shortcuts import render
from django.db import connection
from django.conf import settings
from ex07.models import Movies
from datetime import date
from django import forms

# Create your views here.
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
            Movies.objects.create(**movie)
            messages.append(f"OK : {movie["title"]}")
        except Exception as e:
            messages.append(f"Fail : {movie["title"]}; Reason : {str(e)}")
    return render(request, "ex07/populate.html", {"messages": messages})

def display(request):
    #Throws when table does not exists
    movies = Movies.objects.all()
    return render(request, "ex07/display.html", {"movies": movies})

class DeleteMovie(forms.Form):
    movie = forms.ModelChoiceField(
        queryset=Movies.objects.all(),
        empty_label="Select a movie to remove",
    )

def remove(request):
    if request.method == "POST":
        form = DeleteMovie(request.POST)
        if form.is_valid():
            movie = form.cleaned_data["movie"]
            movie.delete()
    else:
        form = DeleteMovie()
    movies = Movies.objects.all()
    return render(request, "ex07/remove.html", {"movies": movies, "form": form})

class UpdateMovie(forms.Form):
    movie = forms.ModelChoiceField(
        queryset=Movies.objects.all(),
        empty_label="Select a movie to update it's opening crawl",
    )
    opening = forms.CharField()

def update(request):
    if request.method == "POST":
        form = UpdateMovie(request.POST)
        if form.is_valid():
            movie = form.cleaned_data["movie"]
            movie.opening_crawl = form.cleaned_data["opening"]
            movie.save()
    else:
        form = UpdateMovie()
    movies = Movies.objects.all()
    return render(request, "ex07/update.html", {"movies": movies, "form": form})
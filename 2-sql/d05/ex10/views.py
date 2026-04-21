from django.shortcuts import render
from django import forms
from django.forms.widgets import DateInput 
from django.db.models import Prefetch
from ex10.models import People, Planets, Movies

class SearchPeople(forms.Form):
    min_release_date = forms.DateField(
        widget=DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        label="Minimal release date",
        input_formats=["%Y-%m-%d"]
    )
    max_release_date = forms.DateField(
        widget=DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        label="Maximal release date",
        input_formats=["%Y-%m-%d"]
    )
    planet_diameter_gt = forms.IntegerField(
        label="Minimal planet diameter"
    )
    character_gender = forms.ChoiceField(
        choices=[],
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genders = People.objects.distinct("gender").values_list("gender", flat=True)
        self.fields["character_gender"].choices = [("", "Select gender of character")] + [(gender, gender) for gender in genders]

def research(request):
    result = None
    if request.method == "POST":
        is_searched = True
        form = SearchPeople(request.POST)
        if form.is_valid():
            min_release_date = form.cleaned_data["min_release_date"]
            max_release_date = form.cleaned_data["max_release_date"]
            planet_diameter_gt = form.cleaned_data["planet_diameter_gt"]
            character_gender = form.cleaned_data["character_gender"]

            #Many to many is crap to use
            #Make the table explicit and query it like a sane person
            #Read that it can be done with through=
            movies = Movies.objects.filter(
                release_date__gt=min_release_date,
                release_date__lt=max_release_date
            )

            if movies.exists():
                result = People.objects.filter(
                    movies__in=movies,
                    homeworld__diameter__gt=planet_diameter_gt,
                    gender=character_gender,
                ).prefetch_related("homeworld", Prefetch("movies", queryset=movies)).distinct()
            else:
                result=None
    else:
        is_searched = False
        form = SearchPeople()
    return render(request, "ex10/research.html", {"form": form, "result": result, "is_searched": is_searched})
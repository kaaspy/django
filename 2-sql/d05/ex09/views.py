from django.shortcuts import render
from ex09.models import People

def display(request):
    #Throws when table does not exists
    people = People.objects.select_related("homeworld").filter(
        homeworld__climate__contains="windy"
    ).order_by("name")
    return render(request, "ex09/display.html", {"people": people})

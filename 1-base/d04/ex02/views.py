from django.shortcuts import render
from django import forms
import logging

class myform(forms.Form):
    content = forms.CharField(max_length=255)

# Create your views here.
def submit_form(request):
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        form = myform(request.POST)
        logger.info(form.data["content"])
    else:
        form = myform()
    try:
        with open("ex02/logs", "r") as f:
            history = f.read().split("\n")
    except FileNotFoundError:
        history = []
    return render(request, "ex02/submit.html", {"form": form, "history": history})
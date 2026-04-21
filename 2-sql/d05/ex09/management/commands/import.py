import json
from django.core.management.base import BaseCommand
from django.contrib.staticfiles.storage import staticfiles_storage
from ex09.models import Planets, People

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Importing data...\n")
                     
        with open(staticfiles_storage("json/ex09_initial_data.json"))

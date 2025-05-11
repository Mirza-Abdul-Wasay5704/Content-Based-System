import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from RecApp.models import Item_Profile


class Command(BaseCommand):
    help = "Load Preprocessed_items.csv into the database"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(
            settings.BASE_DIR, "RecApp", "data", "Preprocessed_items.csv"
        )

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Item_Profile.objects.update_or_create(
                    title=row["title"],
                    defaults={
                        "ner": row["NER"],
                        "directions": row["directions"],
                        "genre": row["genre"],
                    },
                )
        self.stdout.write(self.style.SUCCESS("Data loaded successfully."))

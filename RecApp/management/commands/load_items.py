import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from RecApp.models import Item_Profile


class Command(BaseCommand):
    help = "Load Preprocessed_items.csv into the database, optimized."

    def handle(self, *args, **kwargs):
        file_path = os.path.join(
            settings.BASE_DIR, "RecApp", "data", "Preprocessed_items.csv"
        )

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            items = []
            processed_lines = 0

            for index, row in enumerate(reader, start=1):
                try:
                    item = Item_Profile(
                        title=row["title"].title(),
                        ner=row["NER"].title(),
                        directions=row["directions"],
                        genre=row["genre"].title(),
                    )
                    items.append(item)

                    if len(items) >= 100:
                        Item_Profile.objects.bulk_create(items)
                        items.clear()

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing row {index}: {e}")
                    )
                    continue

                processed_lines += 1

            if items:
                Item_Profile.objects.bulk_create(items)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Finished loading. Processed {processed_lines} rows."
                )
            )

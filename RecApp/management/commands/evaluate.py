from django.core.management.base import BaseCommand
from RecApp.models import User_Profile
from sklearn.metrics import precision_score, recall_score
from RecApp.vector_db.faiss_handler import FaissHandler


class Command(BaseCommand):
    help = "Evaluates Precision at K, Recall at K, and other metrics"

    def add_arguments(self, parser):
        parser.add_argument(
            "--k",
            type=int,
            default=5,
            help="The K value for Precision at K and Recall at K",
        )

    def handle(self, *args, **kwargs):
        k = kwargs["k"]
        user_profiles = User_Profile.objects.all()

        precision_at_k_values = []
        recall_at_k_values = []

        faiss_handler = FaissHandler(
            "RecApp/vector_db/item_index.faiss", "RecApp/vector_db/titles.txt"
        )

        for user_profile in user_profiles:
            clicked_titles = user_profile.clicked_titles
            user_embedding = user_profile.get_embedding()

            if user_embedding is None or len(user_embedding) == 0:
                continue

            predicted_titles_with_scores = faiss_handler.get_top_k(user_embedding, k)
            predicted_titles = [title for title, _ in predicted_titles_with_scores]

            y_true = [1 if title in clicked_titles else 0 for title in predicted_titles]
            y_pred = [
                1 if title in predicted_titles else 0 for title in predicted_titles
            ]

            precision_at_k = self.calculate_precision_at_k(y_true, y_pred, k)
            recall_at_k = self.calculate_recall_at_k(y_true, y_pred, k)

            precision_at_k_values.append(precision_at_k)
            recall_at_k_values.append(recall_at_k)

        average_precision_at_k = (
            sum(precision_at_k_values) / len(precision_at_k_values)
            if precision_at_k_values
            else 0
        )
        average_recall_at_k = (
            sum(recall_at_k_values) / len(recall_at_k_values)
            if recall_at_k_values
            else 0
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Average Precision at {k}: {average_precision_at_k:.4f}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"Average Recall at {k}: {average_recall_at_k:.4f}")
        )

    def calculate_precision_at_k(self, y_true, y_pred, k):
        return precision_score(y_true[:k], y_pred[:k])

    def calculate_recall_at_k(self, y_true, y_pred, k):
        return recall_score(y_true[:k], y_pred[:k], zero_division=0)

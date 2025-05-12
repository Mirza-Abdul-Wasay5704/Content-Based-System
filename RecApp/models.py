from django.db import models
from django.contrib.auth.models import User
import numpy as np


class Item_Profile(models.Model):
    title = models.CharField(max_length=255, unique=True)
    ner = models.TextField()
    directions = models.TextField()
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    embedding = models.BinaryField(null=True, blank=True)
    survey_completed = models.BooleanField(default=False)
    clicked_titles = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.user.username

    def set_embedding(self, embedding):
        self.embedding = embedding.tobytes()

    def get_embedding(self):
        if self.embedding is None:
            return None
        return np.frombuffer(self.embedding, dtype="float32")

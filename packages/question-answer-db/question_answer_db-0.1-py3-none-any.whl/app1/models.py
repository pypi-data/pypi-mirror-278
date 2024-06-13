from django.db import(models)
from django.contrib.postgres.fields import JSONField

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

class SimilarQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField()

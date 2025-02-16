from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=225, unique=True)
    age = models.IntegerField()

    def __str__(self):
        return self.name
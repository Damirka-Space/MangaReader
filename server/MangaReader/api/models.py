from django.db import models


class Manga(models.Model):
    name = models.CharField(max_length=128)
    chapters_cnt = models.IntegerField()

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title
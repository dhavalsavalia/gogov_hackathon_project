from django.db import models

# Create your models here.


class MainProject(models.Model):
    PROJECT_NAME = models.CharField(max_length=50)
    HOMEPAGE = models.URLField(max_length=100)

    def __str__(self):
        return self.PROJECT_NAME

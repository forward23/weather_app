from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return self.name
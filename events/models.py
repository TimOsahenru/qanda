from django.db import models

# Create your models here.
class Event(models.Model):
    # organizer
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    # questions


    def __str__(self):
        return self.name
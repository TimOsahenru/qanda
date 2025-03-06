from django.db import models
from events.models import Event


class Question(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    # likes = 
    # like_counter = 
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.event.name
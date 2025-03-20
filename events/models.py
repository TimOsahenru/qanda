from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Event(models.Model):
    # organizer
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    # questions


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_details', kwargs={'slug': self.slug})
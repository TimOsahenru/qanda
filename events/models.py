from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from django.core.exceptions import ValidationError


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
        # Generate the slug if it's not provided
        if not self.slug:
            self.slug = slugify(self.name)

        # Check if the slug already exists (excluding the current instance if updating)
        if Event.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError(f'An event with the name "{self.name}" already exists. Consider using a unique name.')

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_details', kwargs={'slug': self.slug})
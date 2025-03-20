from django import forms
from events.models import Event



class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name']
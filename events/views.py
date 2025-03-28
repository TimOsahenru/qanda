from django.shortcuts import render, redirect, get_object_or_404
from events.forms import EventForm, EventEditForm
from events.models import Event

from questions.models import Question
from django.contrib import messages

from django.utils.text import slugify
from django.core.exceptions import ValidationError

def edit_event(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.method == "POST":
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_details', slug=slug)
        
    else:
        form = EventEditForm(instance=event)
    return render(request, 'edit-event.html', {'form': form})


def event_details(request, slug):

    event = get_object_or_404(Event, slug=slug)
    questions = Question.objects.filter(event=event)

    return render(request, 'event-detail.html', {'event': event, 'questions': questions})

def home_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                event.slug = slugify(event.name)

                event.save()

                return redirect('event_details', slug=event.slug)
            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = EventForm()
    return render(request, 'index.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from events.forms import EventForm, EventEditForm
from events.models import Event

from questions.models import Question



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
# Flow
# 1. create event (unique name)
# 2. redirect to the event detail page
# 3. event detailed page should have
    # a. name of event
    # b. url to copy (unique URL)
    # c. url to copy should lead to questions page

# def event_details(request, pk):
def event_details(request, slug):
# def event_details(request, slug):
    # event = Event.objects.get(pk=pk)
    event = get_object_or_404(Event, slug=slug)
    questions = Question.objects.filter(event=event)

    return render(request, 'event-detail.html', {'event': event, 'questions': questions})
    # return render(request, 'create-questions.html', {'event': event, 'questions': questions})

def home_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # check if event.slug exist in db
            # if yes as for a unique name
            # if no
            # create event
            
            event = form.save()
            questions = Question.objects.create(event=event)
            # questions = Question.objects.create(event=event, text=f'Questions for {event.name}')

            return redirect('event_details', slug=event.slug)
            # event = form.save()
            # return redirect(event.get_absolute_url())
            # return redirect('event_details', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'index.html', {'form': form})
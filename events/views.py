from events.models import Event
from events.forms import EventForm
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render, redirect, get_object_or_404


from questions.models import Question
from django.contrib import messages

from django.utils.text import slugify
from django.core.exceptions import ValidationError


def event_details(request, slug):

    event = get_object_or_404(Event, slug=slug)
    questions = Question.objects.filter(event=event)

    return render(request, 'event-detail.html', {'event': event, 'questions': questions})


@ratelimit(key='ip', rate='5/h', method='POST', block=False)
def home_view(request):
    is_limited = getattr(request, 'limited', False)
    if is_limited:
        messages.error(request, "You've reached the maximum of 5 events per hour. Please try again later")
        return render(request, 'index.html', {'form': EventForm()})


    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                event.slug = slugify(event.name)

                event.save()

                return redirect('event_details', slug=event.slug)
            except ValidationError as e:
                messages.error(request, str(e).strip("[]'"))
    else:
        form = EventForm()
    return render(request, 'index.html', {'form': form})

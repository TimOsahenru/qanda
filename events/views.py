from django.shortcuts import render, redirect
from events.forms import EventForm


def home_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/question')
    else:
        form = EventForm()
    return render(request, 'index.html', {'form': form})
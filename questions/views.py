from django.shortcuts import render, redirect, get_object_or_404
from questions.forms import QuestionForm
from events.models import Event
from questions.models import Question


# def create_question(request, pk):
def create_question(request, slug):
    event = get_object_or_404(Event, slug=slug)
    # questions = Question.objects.all()
    questions = Question.objects.filter(event=event)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            question = form.save(commit=False)
            question.event = event
            question.save()
            return redirect('create_question', slug=slug)
            # return redirect('/')
            # return redirect('event_questions', event_name=event.name)
        
    else:
        form = QuestionForm()
    # return render(request, 'create-question.html', {'form': form, 'event': event})
    return render(request, 'create-questions.html', {'form': form, 'questions': questions, 'event': event})


# def questions(request):

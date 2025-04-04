from django.urls import reverse
from events.models import Event
from questions.models import Question
from django.test import TestCase, Client


class CreateQuestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.event = Event.objects.create(name='test event', slug='test-event')
        self.question_1 = Question.objects.create(event=self.event, text='Question 1')
        self.question_2 = Question.objects.create(event=self.event, text='Question 2')

    def test_create_questions_endpoint(self):

        data = {
            'text': 'How to be successful',
        }

        response = self.client.post(reverse('create_question', args=[self.event.slug]), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 3)


    def test_create_questions_is_unique_to_event(self):
        response = self.client.get(reverse('create_question', args=[self.event.slug]))

        event = Event.objects.create(
            name='fake event',
            slug='fake-event'
        )

        question = Question.objects.create(
            text='How to make good money',
            event=event,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(question.event, self.event)
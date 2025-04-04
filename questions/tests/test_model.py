from django.test import TestCase
from events.models import Event
from questions.models import Question


class TestQuestionModelClass(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='afcon 2025',
            slug='afcon-2025',
        )

        self.question = Question.objects.create(
            event=self.event,
            text='How to be successful',
        )

    def test_str_question_method(self):
        self.assertEqual(self.event.name, str(self.question))
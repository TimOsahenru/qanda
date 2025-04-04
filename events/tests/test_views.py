from django.test import TestCase, Client
from django.urls import reverse

from events.models import Event
from questions.models import Question

class CreateEventViewTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_get_request_display_template(self):
        response = self.client.post(reverse('home_view'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_create_event_page_redirects(self):

        data = {
            'name': 'PyConGh 2025',
            'created_at': '2023-10-01 12:00:00',
            'updated_at': '2023-10-01 14:00:00',
            'slug': 'pycongh-2025',
        }

        response = self.client.post(reverse('home_view'), data)
        self.assertEqual(response.status_code, 302)


    def test_error_message_display_in_duplicate_event_names(self):
         
        data = {
            'name': 'PyConGh 2025',
            'created_at': '2023-10-01 12:00:00',
            'updated_at': '2023-10-01 14:00:00',
            'slug': 'pycongh-2025',
        }
        self.client.post(reverse('home_view'), data)

        duplicate_data = {
            'name': 'PyConGh 2025',
            'created_at': '2023-10-01 12:00:00',
            'updated_at': '2023-10-01 14:00:00',
            'slug': 'pycongh-2025',
        }
        response = self.client.post(reverse('home_view'), duplicate_data, follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn(data['name'], str(messages[0]))


class EventDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.event = Event.objects.create(name='test event', slug='test-event')
        self.question_1 = Question.objects.create(event=self.event, text='Question 1')
        self.question_2 = Question.objects.create(event=self.event, text='Question 2')


    def test_event_detail_views(self):
        response = self.client.get(reverse('event_details', args=[self.event.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertIn('questions', response.context)
        self.assertEqual(len(response.context['questions']), 2)
        self.assertQuerySetEqual(response.context['questions'], [self.question_1, self.question_2], ordered=False)
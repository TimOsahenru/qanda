from django.test import TestCase, Client
from django.urls import reverse


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
        
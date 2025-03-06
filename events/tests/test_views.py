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
            'url': 'http://timosahenru.com/'
        }

        response = self.client.post(reverse('home_view'), data)
        self.assertEqual(response.status_code, 302)

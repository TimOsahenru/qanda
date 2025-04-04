from events.models import Event
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError


class TestEventModel(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='afcon 2025',
            slug='afcon-2025',
        )


    def test_event_str_method(self):
        self.assertEqual(str(self.event), 'afcon 2025')

    def test_slug_auto_generate(self):
        event = Event(name='another test event')
        event.save()
        self.assertEqual(event.slug, 'another-test-event')

    def test_get_absolute_url(self):
        expected_url = reverse('event_details', kwargs={'slug': 'afcon-2025'})
        self.assertEqual(self.event.get_absolute_url(), expected_url)
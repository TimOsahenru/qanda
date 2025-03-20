from events.models import Event
from django.test import TestCase


class TestEventModel(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='afcon 2025',
            slug='afcon-2025',
        )


    def test_event_str_method(self):
        self.assertEqual(str(self.event), 'afcon 2025')
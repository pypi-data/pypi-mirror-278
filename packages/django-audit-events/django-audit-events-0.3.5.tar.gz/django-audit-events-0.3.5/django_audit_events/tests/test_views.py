import django_filters
from django.test import override_settings
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from django_audit_events.models import AuditEvent
from django_audit_events.tests.utils.models import Poll
from django_audit_events.views import AuditEventViewSet

if django_filters.VERSION < (2, 0):
    from rest_framework_filters.backends import DjangoFilterBackend
else:
    from django_filters.rest_framework.backends import DjangoFilterBackend


class AuditEventViewSetTestCase(APITestCase):
    def setUp(self):
        self.poll_1 = baker.make(Poll)
        self.poll_2 = baker.make(Poll)
        self.audit_event_1 = baker.make(AuditEvent, content_object=self.poll_1)
        self.audit_event_2 = baker.make(AuditEvent, content_object=self.poll_2)

    @override_settings(ROOT_URLCONF="django_audit_events.urls")
    def test_get_events(self):
        response = self.client.get(reverse("auditevent-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @override_settings(ROOT_URLCONF="django_audit_events.urls")
    def test_get_events_with_object_id(self):
        # Added for filtering
        AuditEventViewSet.filter_backends = [DjangoFilterBackend]

        response = self.client.get(
            reverse("auditevent-list") + "?object_id={}".format(self.poll_1.pk)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

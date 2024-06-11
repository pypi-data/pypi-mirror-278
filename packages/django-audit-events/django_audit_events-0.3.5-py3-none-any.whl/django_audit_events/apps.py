from __future__ import unicode_literals

from distutils.version import StrictVersion

import django

if StrictVersion(django.get_version()) >= StrictVersion("2.0.0"):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class DjangoAuditEventsConfig(AppConfig):
    name = "django_audit_events"
    verbose_name = _("Django Audit Event")

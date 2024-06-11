try:
    from django.urls import include, path
except ImportError:
    from django.conf.urls import include, url as path
from rest_framework.routers import DefaultRouter

from django_audit_events.views import AuditEventViewSet

router = DefaultRouter()
router.register(r"events", AuditEventViewSet)

app_name = "django_audit_events"

urlpatterns = [path("", include(router.urls))]

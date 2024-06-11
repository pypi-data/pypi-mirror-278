import django_filters

from django_audit_events.models import get_audit_event_model

if django_filters.VERSION < (2, 0):
    import rest_framework_filters as PY2Filters

    class AuditEventRestFrameworkFilter(PY2Filters.FilterSet):
        user = PY2Filters.NumberFilter(name="user")
        content_type = PY2Filters.NumberFilter(name="content_type")
        object_id = PY2Filters.NumberFilter(name="object_id")
        timestamp__lt = PY2Filters.DateTimeFilter(name="timestamp", lookup_expr="lt")
        timestamp__gt = PY2Filters.DateTimeFilter(name="timestamp", lookup_expr="gt")
        timestamp__lte = PY2Filters.DateTimeFilter(name="timestamp", lookup_expr="lte")
        timestamp__gte = PY2Filters.DateTimeFilter(name="timestamp", lookup_expr="gte")

        class Meta:
            model = get_audit_event_model()
            fields = ("user", "content_type", "object_id", "timestamp")

    AuditEventFilterSet = AuditEventRestFrameworkFilter

else:
    from django_filters import FilterSet, filters

    class AuditEventDjangoFilter(FilterSet):
        user = filters.NumberFilter(field_name="user")
        content_type = filters.NumberFilter(field_name="content_type")
        object_id = filters.NumberFilter(field_name="object_id")
        timestamp__lt = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lt")
        timestamp__gt = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gt")
        timestamp__lte = filters.DateTimeFilter(
            field_name="timestamp", lookup_expr="lte"
        )
        timestamp__gte = filters.DateTimeFilter(
            field_name="timestamp", lookup_expr="gte"
        )

        class Meta:
            model = get_audit_event_model()
            fields = ("user", "content_type", "object_id", "timestamp")

    AuditEventFilterSet = AuditEventDjangoFilter

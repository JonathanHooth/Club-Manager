from django.contrib import admin

from core.abstracts.admin import ModelAdminBase
from events.models import (
    Event,
    EventAttendance,
    EventAttendanceLink,
    EventHost,
    EventTag,
    RecurringEvent,
)
from events.serializers import EventCsvSerializer
from events.services import EventService


# Register your models here.
class RecurringEventAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "day",
        "location",
        "start_date",
        "end_date",
    )
    actions = ("sync_events",)
    filter_horizontal = ("other_clubs",)

    @admin.action(description="Sync Events")
    def sync_events(self, request, queryset):

        for recurring in queryset.all():
            EventService.sync_recurring_event(recurring)

        return


class EventAttendanceInlineAdmin(admin.TabularInline):
    """List event attendees in event admin."""

    model = EventAttendance
    extra = 0
    readonly_fields = ("created_at",)

    def has_add_permission(self, request, *args, **kwargs):
        return False


class EventAttendenceLinkInlineAdmin(admin.StackedInline):
    """List event links in event admin."""

    model = EventAttendanceLink
    readonly_fields = (
        "target_url",
        "club",
        "tracking_url_link",
    )
    extra = 0

    def tracking_url_link(self, obj):
        return obj.as_html()


class EventHostInlineAdmin(admin.TabularInline):
    """Manage clubs hosting events."""

    model = EventHost
    extra = 1


class EventAdmin(ModelAdminBase):
    """Admin config for club events."""

    csv_serializer_class = EventCsvSerializer

    list_display = (
        "__str__",
        "id",
        "location",
        "start_at",
        "end_at",
    )
    ordering = ("start_at",)

    inlines = (
        EventHostInlineAdmin,
        EventAttendenceLinkInlineAdmin,
        EventAttendanceInlineAdmin,
    )
    filter_horizontal = ("tags",)


admin.site.register(Event, EventAdmin)
admin.site.register(EventTag)
admin.site.register(RecurringEvent, RecurringEventAdmin)

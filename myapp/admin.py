from django.contrib import admin

from .models import (
    UserProfile,
    Alert,
    EmergencyResource,
    HelpRequest
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'role'
    )

    list_filter = (
        'role',
    )

    search_fields = (
        'user__username',
        'phone'
    )


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    list_display = (
        'disaster_type',
        'area',
        'created_by',
        'alert_date'
    )

    list_filter = (
        'disaster_type',
    )


@admin.register(EmergencyResource)
class EmergencyResourceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'resource_type',
        'district',
        'phone',
        'availability'
    )

    list_filter = (
        'resource_type',
        'availability'
    )


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'emergency_type',
        'location',
        'status',
        'handled_by',
        'request_date'
    )

    list_filter = (
        'status',
        'emergency_type'
    )

    search_fields = (
        'user__username',
        'location',
        'phone'
    )
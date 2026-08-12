from django.db import models
from django.contrib.auth.models import User




class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('USER', 'User'),
        ('COORDINATOR', 'Emergency Coordinator'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"




class Alert(models.Model):

    disaster_type = models.CharField(
        max_length=100
    )

    area = models.CharField(
        max_length=200
    )

    alert_message = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    alert_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.disaster_type} - {self.area}"




class EmergencyResource(models.Model):

    RESOURCE_TYPES = [
        ('Hospital', 'Hospital'),
        ('Ambulance', 'Ambulance'),
        ('Police', 'Police'),
        ('Relief Camp', 'Relief Camp'),
        ('Fire Station', 'Fire Station'),
    ]

    name = models.CharField(
        max_length=200
    )

    resource_type = models.CharField(
        max_length=50,
        choices=RESOURCE_TYPES
    )

    address = models.TextField()

    district = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    availability = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.name} - {self.resource_type}"




class HelpRequest(models.Model):

    EMERGENCY_TYPES = [
        ('Flood', 'Flood'),
        ('Fire', 'Fire'),
        ('Earthquake', 'Earthquake'),
        ('Cyclone', 'Cyclone'),
        ('Landslide', 'Landslide'),
        ('Tsunami', 'Tsunami'),
        ('Medical', 'Medical Emergency'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('In Process', 'In Process'),
        ('Completed', 'Completed'),
    ]

    # User who submitted the request
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # User phone number
    phone = models.CharField(
        max_length=15
    )

    # Emergency location
    location = models.CharField(
        max_length=200
    )

    # Type of emergency
    emergency_type = models.CharField(
        max_length=50,
        choices=EMERGENCY_TYPES
    )

    # User's emergency description
    description = models.TextField()

    # Request status
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Received'
    )

    # Help provided by coordinator
    response_result = models.TextField(
        blank=True,
        null=True
    )

    # Coordinator who handled the request
    handled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_requests'
    )

    # Date when request was completed
    completed_date = models.DateTimeField(
        null=True,
        blank=True
    )

    # Date when request was submitted
    request_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.emergency_type}"
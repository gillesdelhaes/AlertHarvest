from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Alert(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('EXPIRED', 'Expired'),
    ]
    SEVERITY_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('MAJOR', 'Major'),
        ('WARNING', 'Warning'),
    ]
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=255)
    severity = models.CharField(max_length=15, choices=SEVERITY_CHOICES, default='WARNING')
    message = models.TextField()
    source = models.TextField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    last_occurrence = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    blackout = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.location} - {self.severity} - {self.message}"
    
    def update_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError("Invalid status value")
        
        self.status = new_status
        self.save()
        
class BlackoutRule(models.Model):
    source = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    message_contains_word = models.CharField(max_length=255, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        super().clean()
        if not any([self.source, self.location, self.message_contains_word]):
            raise ValidationError("At least one of source, location, or message_contains_word must be provided.")
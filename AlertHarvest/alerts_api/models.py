from django.db import models

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
    source = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    last_occurrence = models.DateTimeField(blank=True, null=True)
     
    def __str__(self):
        return f"{self.location} - {self.severity} - {self.message}"

    # def send_alert_notification(self):
    #     if self.severity == "CRITICAL" and not self.acknowledged:
    #         send_alert_email(self)
            
    def update_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError("Invalid status value")
        
        self.status = new_status
        self.save()
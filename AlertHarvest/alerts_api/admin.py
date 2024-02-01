from django.contrib import admin

# Register your models here.
from .models import Alert, BlackoutRule
admin.site.register(Alert)
admin.site.register(BlackoutRule)
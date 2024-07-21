from django import forms
from alerts_api.models import BlackoutRule  # Import the model from the alert_api app

class BlackoutRuleForm(forms.ModelForm):
    class Meta:
        model = BlackoutRule
        fields = ['source', 'location', 'message_contains_word', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        location = cleaned_data.get('location')
        message_contains_word = cleaned_data.get('message_contains_word')

        if not any([source, location, message_contains_word]):
            raise forms.ValidationError("At least one of source, location, or message_contains_word must be provided.")

        return cleaned_data
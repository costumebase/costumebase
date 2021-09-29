from django import forms
from dashboard.models import Messages


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        exclude = ['sender_name',]
        fields = ['description']
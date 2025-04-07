from django import forms

from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M', attrs={'type': 'datetime-local'})
    )
    end_datetime = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M', attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Mailing
        fields = ['start_datetime', 'end_datetime', 'periodicity', 'message', 'clients']

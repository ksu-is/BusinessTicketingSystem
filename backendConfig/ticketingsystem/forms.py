# forms.py
from django import forms
from .models import Ticket, Employee
from django.utils.timezone import now

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticname', 'ticpriority', 'employid']
        labels = {
            'ticname': 'Ticket Subject',
            'ticpriority': 'Priority',
            'employid': 'Employee',
        }

class CloseTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = []  # No fields needed, just closing the ticket

class AcceptTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = []  # No fields needed, just accepting the ticket

    def save(self, commit=True):
        ticket = super().save(commit=False)
        ticket.ticacceptdate = now()  # Set the acceptance date to the current time
        if commit:
            ticket.save()
        return ticket
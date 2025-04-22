# forms.py
from django import forms
from .models import Ticket, Employee

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticname', 'ticpriority', 'employid', 'agentid']
        labels = {
            'ticname': 'Ticket Subject',
            'ticpriority': 'Priority',
            'employid': 'Employee',
            'agentid': 'Assigned Agent',
        }
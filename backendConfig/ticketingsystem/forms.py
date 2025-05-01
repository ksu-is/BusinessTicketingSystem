# forms.py
from django import forms
from .models import Ticket, Employee
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm

class TicketForm(forms.ModelForm):

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter additional details about the ticket...'}),
        required=False,
        label="Comment"
    )

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
    agentid = forms.ModelChoiceField(
    queryset=Employee.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control'}),
    label="Assign Agent"
    )
    class Meta:
        model = Ticket
        fields = ['agentid']

    def save(self, commit=True):
        ticket = super().save(commit=False)
        ticket.ticacceptdate = now()  # Set the acceptance date to the current time
        if commit:
            ticket.save()
        return ticket
    
class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
        label="Email"
    )
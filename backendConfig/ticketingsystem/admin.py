from django.contrib import admin
from .models import Branch, Employee, Ticket, Comment, Ticketmetrics

# Register your models here.

admin.site.register(Branch)
admin.site.register(Employee)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Ticketmetrics)
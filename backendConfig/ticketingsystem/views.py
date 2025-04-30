from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ticket, Employee, Branch, Comment, Ticketmetrics
from django.http import HttpResponse
from django.utils import timezone
from .forms import TicketForm

# Create your views here.

def home(request):
    return render(request, "home.html")

# views.py

def ticket_list(request):
    tickets_list = Ticket.objects.all().order_by('-ticcreatedate')
    
    # Search functionality
    query = request.GET.get('query')
    if query:
        tickets_list = tickets_list.filter(
            Q(ticid__icontains=query) |
            Q(ticname__icontains=query) |
            Q(employid__employname__icontains=query) |
            Q(employid__deptname__icontains=query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'open':
        tickets_list = tickets_list.filter(ticacceptdate__isnull=True)
    elif status_filter == 'in-progress':
        tickets_list = tickets_list.filter(ticacceptdate__isnull=False, ticclosetime__isnull=True)
    elif status_filter == 'resolved':
        tickets_list = tickets_list.filter(ticclosetime__isnull=False)
    
    # Pagination
    paginator = Paginator(tickets_list, 10)  # Show 10 tickets per page
    page = request.GET.get('page')
    tickets = paginator.get_page(page)
    
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

def ticket_detail(request, ticid):
    ticket = get_object_or_404(Ticket, ticid=ticid)
    comments = Comment.objects.filter(ticid=ticket)
    
    try:
        metrics = Ticketmetrics.objects.get(ticid=ticket)
    except Ticketmetrics.DoesNotExist:
        metrics = None
    
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'metrics': metrics
    })

def ticket_create(request):
    print("ticket_create view called")  # Debug statement
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Generate a new ticket ID (you might want to customize this)
            last_ticket = Ticket.objects.order_by('-ticid').first()
            if last_ticket:
                new_id = str(int(last_ticket.ticid) + 1).zfill(7)
            else:
                new_id = '0000001'
            
            ticket.ticid = new_id
            ticket.ticcreatedate = timezone.now()
            ticket.save()
            return redirect('ticket_detail', ticid=ticket.ticid)
    else:
        form = TicketForm()
    
    return render(request, 'tickets/ticket_create.html', {'form': form})
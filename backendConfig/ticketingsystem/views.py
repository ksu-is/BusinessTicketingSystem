from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ticket, Employee, Branch, Comment, Ticketmetrics
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import now
from .forms import TicketForm, CloseTicketForm

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

    metrics = None
    if ticket.ticclosetime:
        try:
            metrics = Ticketmetrics.objects.get(ticid=ticket, ticclosetime=ticket.ticclosetime)
        except Ticketmetrics.DoesNotExist:
            metrics = None

    # Check if the ticket is being closed
    if request.method == 'POST':
        form = CloseTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            # Generate the close time
            close_time = now()

            # Create a Ticketmetrics entry with the concatenated primary keys
            Ticketmetrics.objects.create(
                ticclosetime=close_time,  # Use the generated close time
                ticid=ticket,  # Use the ticket's ID
                agentid=ticket.agentid,  # Assign the agent handling the ticket
                satisfaction='N',  # Default satisfaction value
            )

            # Update the close time for the ticket
            ticket.ticclosetime = close_time
            ticket.save()

            return redirect('ticket_detail', ticid=ticket.ticid)
    else:
        form = CloseTicketForm(instance=ticket)

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'metrics': metrics,
        'form': form,
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
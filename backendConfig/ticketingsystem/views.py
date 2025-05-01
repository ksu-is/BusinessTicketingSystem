from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ticket, Employee, Branch, Comment, Ticketmetrics
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.views import LoginView
from .forms import TicketForm, CloseTicketForm, AcceptTicketForm, EmailLoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@login_required
def home(request):
    return render(request, "home.html")

# views.py

@login_required
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
    if status_filter == 'Open':
        tickets_list = tickets_list.filter(ticacceptdate__isnull=True)
    elif status_filter == 'In-Progress':
        tickets_list = tickets_list.filter(ticacceptdate__isnull=False, ticclosetime__isnull=True)
    elif status_filter == 'Resolved':
        tickets_list = tickets_list.filter(ticclosetime__isnull=False)
    
    # Pagination
    paginator = Paginator(tickets_list, 10)  # Show 10 tickets per page
    page = request.GET.get('page')
    tickets = paginator.get_page(page)
    
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticid):
    ticket = get_object_or_404(Ticket, ticid=ticid)
    comments = Comment.objects.filter(ticid=ticket)

    metrics = None
    if ticket.ticclosetime:
        try:
            metrics = Ticketmetrics.objects.get(ticid=ticket, ticclosetime=ticket.ticclosetime)
        except Ticketmetrics.DoesNotExist:
            metrics = None

    if request.method == 'POST':
        if 'accept_ticket' in request.POST:  # Handle ticket acceptance
            accept_form = AcceptTicketForm(request.POST, instance=ticket)
            if accept_form.is_valid():
                accept_form.save()
                return redirect('ticket_detail', ticid=ticket.ticid)
        elif 'close_ticket' in request.POST:  # Handle ticket closure
            close_form = CloseTicketForm(request.POST, instance=ticket)
            if close_form.is_valid():
                close_time = now()
                Ticketmetrics.objects.create(
                    ticclosetime=close_time,
                    ticid=ticket,
                    agentid=ticket.agentid,
                    satisfaction='N',
                )
                ticket.ticclosetime = close_time
                ticket.save()
                return redirect('ticket_detail', ticid=ticket.ticid)
    else:
        accept_form = AcceptTicketForm(instance=ticket)
        close_form = CloseTicketForm(instance=ticket)

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'metrics': metrics,
        'accept_form': accept_form,
        'close_form': close_form,
    })

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            last_ticket = Ticket.objects.order_by('-ticid').first()
            if last_ticket:
                new_id = str(int(last_ticket.ticid) + 1).zfill(7)
            else:
                new_id = '0000001'
            
            ticket.ticid = new_id
            ticket.ticcreatedate = timezone.now()
            ticket.save()

            comment_text = form.cleaned_data.get('comment')
            if comment_text:
                Comment.objects.create(
                    commentid='01',  # You can implement logic to generate unique comment IDs
                    ticid=ticket,
                    employid=ticket.employid,
                    comments=comment_text
                )
            return redirect('ticket_detail', ticid=ticket.ticid)
    else:
        form = TicketForm()
    
    return render(request, 'tickets/ticket_create.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'tickets/login.html'
    authentication_form = EmailLoginForm
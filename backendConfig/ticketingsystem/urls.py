from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tickets/", views.ticket_list, name='ticket_list'),
    path('ticket/<str:ticid>/', views.ticket_detail, name='ticket_detail'),
    # Add this later after implementing the view
    path('ticket/create/', views.ticket_create, name='ticket_create'),    
]
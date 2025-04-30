from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tickets/", views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),  
    path('tickets/<str:ticid>/', views.ticket_detail, name='ticket_detail'),
]
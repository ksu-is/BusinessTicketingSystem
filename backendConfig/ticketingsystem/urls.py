from django.urls import path
from . import views
from .views import CustomLoginView
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url='/login/', permanent=False), name="root_redirect"),
    path('home/', views.home, name="home"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("tickets/", views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),  
    path('tickets/<str:ticid>/', views.ticket_detail, name='ticket_detail'),
]
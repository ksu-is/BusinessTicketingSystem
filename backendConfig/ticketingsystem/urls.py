from django.urls import path
from . import views
from .views import CustomLoginView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", RedirectView.as_view(url='/login/', permanent=False), name="root_redirect"),
    path('home/', views.home, name="home"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("tickets/", views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),  
    path('tickets/<str:ticid>/', views.ticket_detail, name='ticket_detail'),
]
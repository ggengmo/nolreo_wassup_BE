from django.urls import path

from . import views

app_name = 'pick'

urlpatterns = [
    path('lodging/', views.lodging_pick, name='lodging_pick_cl'),
    path('lodging/<int:pk>/', views.lodging_pick, name='lodging_pick_d'),
    path('bus/', views.bus_pick, name='bus_pick_cl'),
    path('bus/<int:pk>/', views.bus_pick, name='bus_pick_d'),
]
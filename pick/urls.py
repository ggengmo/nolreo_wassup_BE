from django.urls import path

from . import views

app_name = 'pick'

urlpatterns = [
    path('lodging/', views.lodging_pick, name='lodging_pick'),
    path('lodging/<int:pk>/', views.lodging_pick, name='lodging_pick_patch'),
    path('bus/', views.bus_pick, name='bus_pick'),
]
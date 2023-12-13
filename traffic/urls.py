from django.urls import path
from . import views

urlpatterns = [
    path('bus/', views.bus, name='bus'),
    path('train/', views.train, name='train'),
]

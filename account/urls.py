from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('refresh/', views.refresh, name='refresh'),
    path('<int:pk>/', views.user, name='user'),
    path('<int:pk>/password/', views.password, name='password'),
]
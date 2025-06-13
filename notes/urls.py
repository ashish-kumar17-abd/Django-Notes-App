from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete/<int:pk>/', views.delete_note, name='delete_note'),

]

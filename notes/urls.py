from django.urls import path
from . import views
from .views import contact_view
from .views import about


urlpatterns = [
    path('', views.home, name='home'),
    path('edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('pin/<int:pk>/', views.toggle_pin, name='toggle_pin'),
    path('contact/', contact_view, name='contact'),
    path('about/', about, name='about'),

]

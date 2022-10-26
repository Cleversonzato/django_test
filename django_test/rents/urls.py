
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rental/', views.rental_view, name='rental'),
    path('rental/create/', views.rental_create, name='rental_create'),
    path('rental/remove/<int:id>', views.rental_remove, name='rental_remove'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('reservation/create/', views.reservation_create, name='reservation_create'),
    path('reservation/remove/<int:id>', views.reservation_remove, name='reservation_remove'),
]


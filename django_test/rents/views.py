"""As a note, since this is a test, I am not following any particular pattern, neither considering too much possible errorsm 
but in production it is best to create some guards and use something like a REST pattern"""

from datetime import datetime
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Rental, Reservation


def index(request):    
    """ Index view, with all the information""" 
    list_all_info = []
    for rental in Rental.objects.all():
        # considering that the reservations are already sorted, we can simply get the privious one like this
        previous_reservation = '-'
        for reservation in rental.reservations:     
            list_all_info.append((rental, reservation, previous_reservation))            
            previous_reservation = reservation.id

    return render(
        request,
        'index.html',
        {'all_rental_info':list_all_info}
    )


def reservation_view(request):
    """ reservations view """
    all_reservation_info = Reservation.objects.all()
    all_rental_info = Rental.objects.all()

    return render(
        request,
        'reservation.html',
        {
            'all_reservation_info':all_reservation_info,
            'all_rental_info':all_rental_info
        }
    )

@require_http_methods(["POST"])
def reservation_create(request):
    """ view to create reservations"""
    success= None
    error = None

    print(request.POST)
    if request.POST['rental_id'] == '' or request.POST['check_in'] == '' or request.POST['check_out'] == '':
        error = 'All fields must have a value'

    else:
        check_in = datetime.strptime(request.POST['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.POST['check_out'], '%Y-%m-%d').date()
        rental_id = request.POST['rental_id']
        if(check_in > check_out):
            error = 'You must enter before you leave'   

        else:
            Reservation.objects.create(check_in=check_in, check_out=check_out, rental_id=rental_id)
            success = True     

    all_reservation_info = Reservation.objects.all()
    all_rental_info = Rental.objects.all()

    return render(
        request,
        'reservation.html',
        {
            'all_reservation_info':all_reservation_info,
            'all_rental_info':all_rental_info,
            'success':success,
            'error':error
        }
    )

def reservation_remove(request, id):
    """view to remove reservations"""
    Reservation.objects.get(pk=id).delete()
    all_reservation_info = Reservation.objects.all()
    all_rental_info = Rental.objects.all()

    return render(
        request,
        'reservation.html',
        {
            'all_reservation_info':all_reservation_info,
            'all_rental_info':all_rental_info,
            'success': True
        }
    )

def rental_view(request):
    """Rental's index view """
    all_rental_info = Rental.objects.all()

    return render(
        request,
        'rental.html',
        {
            'all_rental_info':all_rental_info
        }
    )

@require_http_methods(["POST"])
def rental_create(request):
    """view to create rentals"""
    success = None
    error = None

    if request.POST['name'] != '':
        r = Rental.objects.create(name = request.POST['name'])
        success = True
    else:
        error = 'This field must have a value'

    all_rental_info = Rental.objects.all()

    return render(
        request,
        'rental.html',
        {
            'all_rental_info':all_rental_info,
            'success': success,
            'error': error
        }
    )

def rental_remove(request, id):
    """view to remove rentals"""
    Rental.objects.get(pk=id).delete()
    all_rental_info = Rental.objects.all()

    return render(
        request,
        'rental.html',
        {
            'all_rental_info':all_rental_info,
            'success': True
        }
    )
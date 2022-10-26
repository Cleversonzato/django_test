from datetime import date
from django.test import TestCase
from django.test import Client
from .models import Rental, Reservation
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

#suport functions
def create_rents(id):
    return Rental.objects.create( name='test', id=id )

def create_reservation(id):
    return Reservation.objects.create(check_in='2022-01-01', check_out='2022-02-01', rental_id=id, id=id)


#test classes
class RentTest(TestCase):
    """Basic create/remove test"""
    def test_create_remove(self):
        for i in range(0,2):
            r = create_rents(i)
            self.assertEqual( Rental.objects.get(pk=i).name, 'test' )          
            r.delete()
            self.assertRaises(ObjectDoesNotExist, Rental.objects.get, pk=i)
            

class ReservationTest(TestCase):
    """Basic create/remove test"""
    def test_create_remove(self):
        for i in range(0,2):
            r = create_rents(i)
            create_reservation(i)
            self.assertEqual( Reservation.objects.get(pk=i).check_in, date(2022, 1, 1) )          
            r.delete()            
            self.assertRaises(ObjectDoesNotExist, Reservation.objects.get, pk=i)


class ClientTest(TestCase):
    client = Client()

    def test_integrated(self):     
        #Rentals   
        create_response = self.client.post(reverse('rental_create'), {'name':'test_1'})
        self.assertEqual(create_response.context['all_rental_info'][0].name, 'test_1')

        create_response = self.client.post(reverse('rental_create'), {'name':'test_2'})
        self.assertEqual(create_response.context['all_rental_info'][1].name, 'test_2')

        #Reservations and ordering by check in (does not matter the reservation id, in this case)
        create_response = self.client.post(reverse('reservation_create'), {'check_in':'2022-01-01', 'check_out':'2022-02-02', 'rental_id':1})
        self.assertEqual(create_response.context['all_reservation_info'][0].check_in, date(2022, 1, 1))

        create_response = self.client.post(reverse('reservation_create'), {'check_in':'2022-03-03', 'check_out':'2022-04-04', 'rental_id':1})
        self.assertEqual(create_response.context['all_reservation_info'][1].check_in, date(2022, 3, 3))

        create_response = self.client.post(reverse('reservation_create'), {'check_in':'2021-02-02', 'check_out':'2021-03-03', 'rental_id':1})
        self.assertEqual(create_response.context['all_reservation_info'][0].check_in, date(2021, 2, 2))

        create_response = self.client.post(reverse('reservation_create'), {'check_in':'2022-04-04', 'check_out':'2022-05-05', 'rental_id':1})
        self.assertEqual(create_response.context['all_reservation_info'][3].check_in, date(2022, 4, 4))

        create_response = self.client.post(reverse('reservation_create'), {'check_in':'2022-02-03', 'check_out':'2022-03-04', 'rental_id':2})
        self.assertEqual(create_response.context['all_reservation_info'][4].check_in, date(2022, 4, 4))


        #check previous reservation logic
        index_response = self.client.get(reverse('index'))
        self.assertEqual( index_response.context['all_rental_info'][0][2], '-' )
        self.assertEqual( index_response.context['all_rental_info'][1][2], index_response.context['all_rental_info'][0][1].id )
        self.assertEqual( index_response.context['all_rental_info'][2][2], index_response.context['all_rental_info'][1][1].id )
        self.assertEqual( index_response.context['all_rental_info'][3][2], index_response.context['all_rental_info'][2][1].id )
        self.assertEqual( index_response.context['all_rental_info'][4][2], '-' )
        

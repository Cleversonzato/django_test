from django.db import models

class Rental(models.Model):
    name = models.CharField(max_length=300)

    @property
    def reservations(self):        
        if self.reservation_set.all():
            return self.reservation_set.all()
        else:
            return [Reservation(check_in='', check_out='', id='')]
        

class Reservation(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)

    class Meta:
        ordering = ['check_in']


from django.db import models 
from api.models import User, Event
from django.utils import timezone

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    name = models.CharField(max_length=204)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_available(self, amount=1):
        return self.quantity >= amount and self.event.is_active()
    
    def book(self, user, amount=1):

        if not self.event.is_active():
            return None, "Events Ended"
        
        if self.quantity <=0:
            return None, "Tickets are out"
        
        if self.quantity < amount:
            return None, f"Only {self.quantity} tickets available"

        self.quantity -= amount
        self.save()

        booking = Booking.objects.create(
            ticket = self,
            user = user,
            quantity = amount
        )
        return booking, "Tickets booked successfully"
    
    def __str__(self):
        return f"{self.name} | {self.event.title}"
    

class Booking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    quantity = models.PositiveIntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.ticket.name} | {self.quantity}"
    
        
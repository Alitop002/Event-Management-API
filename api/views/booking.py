from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.models import Ticket, Event, DONE, Booking
from drf_spectacular.utils import extend_schema
from api.serializers import TicketSerializer, BookingSerializer
from api.utils import CustmResponse
from django.utils import timezone


@extend_schema(tags=['Ticket'])
class OwnerTicketApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TicketSerializer

    def get_user(self, user):
        return Ticket.objects.filter(event__user=user)
    
    def get(self, request):
        tickets = self.get_user(request.user)
        serializer = self.serializer_class(tickets, many=True)
        return CustmResponse.success(status=True, message="Your tickets retrieved", data=serializer.data)
    
    def post(self, request):
        if request.user.status != DONE:
            return CustmResponse.error("Only verifired users can create tickets")
        
        event_id = request.data.get("event")
        try:
            event =Event.objects.get(id=event_id, user=request.user)
        except Event.DoesNotExist:
            return CustmResponse.error(message="You can only create tickets for your own events")
        if event.end_time < timezone.now():
            return CustmResponse.error("Cannot create tickets for past events")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("Event end_time:", event.end_time)
        print("Now:", timezone.now())

        return CustmResponse.success(True, "Ticket created successfully", serializer.data)
 
@extend_schema(tags=['Ticket'])   
class OwnerTicketDeletePutApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TicketSerializer

    def get_object(self, pk, user):
        try:
            return Ticket.objects.get(pk=pk, event__user=user)
        except Ticket.DoesNotExist:
            return None
        
    def put(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if not ticket:
            return CustmResponse.error("Ticket not found")
        
        if ticket.event.end_time < timezone.now():
            return CustmResponse.error("Cannot update tickets for past events")
        
        serilizer = self.serializer_class(ticket, data=request.data, partial=True)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return  CustmResponse.success(True, "Ticket updated successfully", serilizer.data)
    
    def delete(self, request, pk):
        ticket = self.get_object(pk, request.user)
        if not ticket:
            return CustmResponse.error("Ticket not found")
        ticket.delete()
        return CustmResponse.success(status=True,message="Ticket deleted successfully")   
    
@extend_schema(tags=['Booking'])  
class BookingCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BookingSerializer

    def get(self,request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = self.serializer_class(bookings, many=True)
        return CustmResponse.success(True, "Your bookings retrieved", serializer.data)

    def post(self, request):
        ticket_id = request.data.get("ticket")
        amount = request.data.get("amout", 1)

        try:
            amount = int(amount)
            if amount <0:
                return CustmResponse.error("Amount must be at least 1")
        except:
            return CustmResponse.error("Amount must be a valid integer")

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return CustmResponse.error("Ticket not found")
        
        if ticket.event.user == request.user:
            return CustmResponse.error("You cannot book tickets for your own event")
        
        booking, msg = ticket.book(request.user, amount)

        if not booking:
            return CustmResponse.error(msg)
        
        serializer = self.serializer_class(booking)
        return CustmResponse.success(True, msg, serializer.data)
        
        

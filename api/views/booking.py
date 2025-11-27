from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.models import Ticket, Event, DONE
from drf_spectacular.utils import extend_schema
from api.serializers import TicketSerializer, BookingSerializer
from api.utils import CustmResponse


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
            event = Event.objects.get(id=event_id, user=request.user)
        except Event.DoesNotExist:
            return CustmResponse.error(message="You can only create tickets for your own events")
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustmResponse(True, "Ticket created successfully", serializer.data)
    
class OwnerTicketDeletePutApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TicketSerializer

    def get_object(self, pk, user):
        try:
            return Ticket.objects.get(pk=pk, event__user=user)
        except Ticket.DoesNotExist:
            return None
        


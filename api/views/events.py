from rest_framework.views import APIView
from api.utils import CustmResponse
from rest_framework.permissions import IsAuthenticated
from api.models import DONE, User, Category, Event
from api.serializers import EventSerializer, CategorySerializer
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser


@extend_schema(tags=['Event'])
class EventListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]
    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'},
                    'category': {'type': 'integer'},
                    'start_time': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2025-11-26T23:11'   # ← БЕЗ Z !
                    },
                    'end_time': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2025-11-26T23:12'
                    }
                }
            }
        }
    )


    def get(self, request):
        events = Event.objects.all()
        serializer = self.serializer_class(events, many=True)
        return CustmResponse.success(
            status=True,
            message="Event list retrieved successfully",
            data = serializer.data
        )
    
    def post(self, request):
        if request.user.status != DONE:
            return CustmResponse.error(
                message="Only verified users can create events."
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return CustmResponse.success(
            status=True,
            message="Event created successfully",
            data=serializer.data
        )
    
@extend_schema(tags=['Event'])
class EventUpdateDeletegetoneApiView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return None
        
    def get(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return CustmResponse.error(
                message="Event not found."
            )
        
        serializer = self.serializer_class(event)
        return CustmResponse.success(
            status=True,
            message="Event retrieved successfully.",
            data=serializer.data
        )
    
    def put(self, request, pk):
        event = self.get_object(pk)
        if not event:
           return CustmResponse.error(
                message="Event not found."
            )
        
        if event.user != request.user or request.user.status != DONE:
            return CustmResponse.error(
                message="You are not allowed to update this event."
            )
        
        serializer = self.serializer_class(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustmResponse.success(
            status=True,
            message="Event updated successfully",
            data=serializer.data
        )
    
    def delete(self, request, pk):
        event = self.get_object(pk)
        if not event:
            return CustmResponse.error(
                message="Event not found"
            )
        
        if event.user != request.user or request.user.status != DONE:
            return CustmResponse.error(
                status=False,
                message="You are not allowed to delete this event."
            )

        event.delete()
        return CustmResponse.success(
            status=True,
            message="Event deleted successfully"
        )
    
@extend_schema(tags=['Event'])
class CategoryListCreateAPIView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return CustmResponse.success(
            status=True,
            message="Categories retrieved successfully",
            data=serializer.data
        )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustmResponse.success(
            status=True,
            message="Category created successfully",
            data=serializer.data
        )
    
@extend_schema(tags=['Event'])
class CategoryDetailApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class =  CategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None
        
    def get(self, request, pk):
        category =  self.get_object(pk)
        if not category:
            return CustmResponse.error(status=False, message="Category not found")
        serializer = self.serializer_class(category)
        return CustmResponse.success(status=True, message="",data=serializer.data )
    
    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return CustmResponse.error(status=False, message="Category not found")
        serializer = self.serializer_class(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustmResponse.success(status=True, message="Category updated", data=serializer.data)
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return CustmResponse.error(status=False, message="Category not found")
        category.delete()
        return CustmResponse.success(status=True, message="Category deleted")


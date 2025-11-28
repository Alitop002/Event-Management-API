from rest_framework.views import APIView
from api.utils import CustmResponse
from rest_framework.permissions import IsAuthenticated
from api.models import DONE, User, Category, Event
from api.serializers import EventSerializer, CategorySerializer
from drf_spectacular.utils import extend_schema
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination



@extend_schema(tags=['Event'])
class EventListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            events = Event.objects.filter(Q(title__icontains=query))
        else:
            events = Event.objects.all()
        
        serializer = self.serializer_class(events, many=True)
        return CustmResponse.success(
            status=True,
            message=f"Found {events.count()} events",
            data = serializer.data
        )
    
    def post(self, request):
        if request.user.status != DONE:
            return CustmResponse.error("Only verified users can create events")
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return CustmResponse.success(
            status=True,
            message="Event created successfully",
            data=serializer.data
        )
    

    
@extend_schema(tags=['Event'])
class EventFilterPaginationApiVIew(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EventSerializer

    def get(self, request):
        category_id = request.GET.get('category', None)
        events = Event.objects.all()

        if category_id:
            events= events.filter(category_id=category_id)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result = paginator.paginate_queryset(events, request)
        serializer = self.serializer_class(result, many=True)

        return paginator.get_paginated_response(serializer.data)
    
@extend_schema(tags=['Event'])
class EventUpdateDeletegetoneApiView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk, user):
        try:
            return Event.objects.get(pk=pk, user=user)
        except Event.DoesNotExist:
            return None
        
    def get(self, request, pk):
        event = self.get_object(pk, request.user)
        if not event:
            return CustmResponse.error(
                message="Event not found or you are not allowed to access it."
            )
        
        serializer = self.serializer_class(event)
        return CustmResponse.success(
            status=True,
            message="Event retrieved successfully.",
            data=serializer.data
        )
    
    def put(self, request, pk):
        event = self.get_object(pk, request.user)
        if not event:
           return CustmResponse.error(
                message="Event not found or you are not allowed to access it."
            )
        
        if request.user.status != DONE:
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
        event = self.get_object(pk, request.user)
        if not event:
            return CustmResponse.error(
                message="Event not found or you are not allowed to access it."
            )
        
        if request.user.status != DONE:
            return CustmResponse.error(
                status=False,
                message="You are not allowed to delete this event."
            )

        event.delete()
        return CustmResponse.success(
            status=True,
            message="Event deleted successfully"
        )
    
@extend_schema(tags=['Category'])
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
    
@extend_schema(tags=['Category'])
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


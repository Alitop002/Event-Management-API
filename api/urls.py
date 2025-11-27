from django.urls import path
from api.views import SendEmailRegistrationAPiView, CodeVerifiredAPiView, ResendCodeAPIView, FullSignUpAPIView, EventListCreateApiView, LoginAPIView\
,EventUpdateDeletegetoneApiView, CategoryDetailApiView, CategoryListCreateAPIView, EventFilterPaginationApiVIew\
,OwnerTicketApiView

urlpatterns = [
    # Auth
    path('Register/', SendEmailRegistrationAPiView.as_view()),
    path('code-verifired/', CodeVerifiredAPiView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('full-register/', FullSignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    # Event Category
    path('Event-get-create/', EventListCreateApiView.as_view()),
    path('Event-update-Delete/<int:pk>/', EventUpdateDeletegetoneApiView.as_view()),
    path('Category-Create/', CategoryListCreateAPIView.as_view()),
    path('Category-Delete/<int:pk>/', CategoryDetailApiView.as_view()),
    #pagination filter
    path('event-filter-pagination/', EventFilterPaginationApiVIew.as_view()),
    # Ticket booking
    path('owner-tickets/', OwnerTicketApiView.as_view()),

    
]

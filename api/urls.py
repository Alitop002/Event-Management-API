from django.urls import path
from api.views import SendEmailRegistrationAPiView, CodeVerifiredAPiView, ResendCodeAPIView, FullSignUpAPIView, EventListCreateApiView, LoginAPIView\
,EventUpdateDeletegetoneApiView, CategoryDetailApiView, CategoryListCreateAPIView

urlpatterns = [
    path('Register/', SendEmailRegistrationAPiView.as_view()),
    path('code-verifired/', CodeVerifiredAPiView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('full-register/', FullSignUpAPIView.as_view()),
    path('Event-get-create/', EventListCreateApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('Event-update-Delete/', EventUpdateDeletegetoneApiView.as_view()),
    path('Category-Create/', CategoryListCreateAPIView.as_view()),
    path('Category-Delete/', CategoryDetailApiView.as_view()),

]

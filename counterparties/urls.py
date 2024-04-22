from django.urls import path
from .views import CounterpartyListAPIView, CounterpartyDetailAPIView, \
    AgreementListAPIView, AgreementDetailAPIView, ContactPersonListAPIView, \
    ContactPersonDetailAPIView, ContactListAPIView, ContactDetailAPIView


urlpatterns = [
    path('vendors/', CounterpartyListAPIView.as_view()),
    path('vendors/<str:pk>/', CounterpartyDetailAPIView.as_view()),
    path('agreements/', AgreementListAPIView.as_view()),
    path('agreements/<str:pk>/', AgreementDetailAPIView.as_view()),
    path('contact_persons/', ContactPersonListAPIView.as_view()),
    path('contact_persons/<str:pk>/', ContactPersonDetailAPIView.as_view()),
    path('contacts/', ContactListAPIView.as_view()),
    path('contacts/<str:pk>/', ContactDetailAPIView.as_view()),
]
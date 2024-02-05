from django.urls import path
from .views import CounterpartyListAPIView, CounterpartyDetailAPIView


urlpatterns = [
    path('vendors/', CounterpartyListAPIView.as_view()),
    path('vendors/<str:pk>/', CounterpartyDetailAPIView.as_view())
]
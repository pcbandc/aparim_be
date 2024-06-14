from django.urls import path
from .views import WarehouseListAPIView, WarehouseDetailAPIView, CategoryListAPIView, \
    CategoryDetailAPIView, UomListAPIView, UomDetailAPIView, GoodListAPIView, \
    GoodDetailAPIView


urlpatterns = [
    path('warehouses/', WarehouseListAPIView.as_view()),
    path('warehouses/<str:pk>/', WarehouseDetailAPIView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<str:pk>/', CategoryDetailAPIView.as_view()),
    path('uoms/', UomListAPIView.as_view()),
    path('uoms/<str:pk>/', UomDetailAPIView.as_view()),
    path('goods/', GoodListAPIView.as_view()),
    path('goods/<str:pk>/', GoodDetailAPIView.as_view()),
]
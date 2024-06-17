from django.urls import path
from .views import WarehouseListAPIView, WarehouseDetailAPIView, CategoryListAPIView, \
    CategoryDetailAPIView, UomListAPIView, UomDetailAPIView, GoodListAPIView, \
    GoodDetailAPIView, StockCardListAPIView, StockCardDetailAPIView, \
    DocumentListAPIView, DocumentDetailAPIView, GoodTransactionListAPIView, \
    GoodTransactionDetailAPIView, DocumentLineListAPIView, DocumentLineDetailAPIView, \
    post_vendors_invoice, unpost_vendors_invoice, post_customers_invoice


urlpatterns = [
    path('warehouses/', WarehouseListAPIView.as_view()),
    path('warehouses/<str:pk>/', WarehouseDetailAPIView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<str:pk>/', CategoryDetailAPIView.as_view()),
    path('uoms/', UomListAPIView.as_view()),
    path('uoms/<str:pk>/', UomDetailAPIView.as_view()),
    path('goods/', GoodListAPIView.as_view()),
    path('goods/<str:pk>/', GoodDetailAPIView.as_view()),
    path('stock_cards/', StockCardListAPIView.as_view()),
    path('stock_cards/<str:pk>/', StockCardDetailAPIView.as_view()),
    path('documents/', DocumentListAPIView.as_view()),
    path('documents/<str:pk>/', DocumentDetailAPIView.as_view()),
    path('good_transactions/', GoodTransactionListAPIView.as_view()),
    path('good_transactions/<str:pk>/', GoodTransactionDetailAPIView.as_view()),
    path('document_lines/', DocumentLineListAPIView.as_view()),
    path('document_lines/<str:pk>/', DocumentLineDetailAPIView.as_view()),
    path('vendors_invoice/post/', post_vendors_invoice),
    path('vendors_invoice/unpost/', unpost_vendors_invoice),
    path('customers_invoice/post/', post_customers_invoice),
]
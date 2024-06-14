from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Warehouse, Category, Uom, Good, StockCard, Document, \
    GoodTransaction, DocumentLine
from .serializers import WarehouseSerializer, CategorySerializer, UomSerializer, \
    GoodSerializer, StockCardSerializer, DocumentSerializer, GoodTransactionSerializer,\
    DocumentLineSerializer


# ***************************** Warehouse API view *************************************
class WarehouseListAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]


class WarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def delete(self, request, pk, format=None):
        warehouse = Warehouse.objects.filter(public_id=pk)
        if warehouse:
            warehouse.delete()
            return HttpResponse(f'The warehouse with id: {pk} has been deleted.')
        return HttpResponse(f'The warehouse with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        warehouse = Warehouse.objects.get(public_id=pk)
        if warehouse:
            serializer = WarehouseSerializer(warehouse)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        warehouse = Warehouse.objects.get(public_id=pk)
        if warehouse:
            serializer = WarehouseSerializer(warehouse, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** Category API view *************************************
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            parent_public_id = request.data['parent']
            parent = Category.objects.get(public_id=parent_public_id)
            serializer.save(parent=parent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def delete(self, request, pk, format=None):
        category = Category.objects.filter(public_id=pk)
        if category:
            category.delete()
            return HttpResponse(f'The category with id: {pk} has been deleted.')
        return HttpResponse(f'The category with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        category = Category.objects.get(public_id=pk)
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        category = Category.objects.get(public_id=pk)
        parent_public_id = request.data['parent']
        if category:
            serializer = CategorySerializer(category, data=request.data)
            parent = Category.objects.get(public_id=parent_public_id)
            if serializer.is_valid():
                serializer.save(parent=parent)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** Uom API view *************************************
class UomListAPIView(generics.ListCreateAPIView):
    queryset = Uom.objects.all()
    serializer_class = UomSerializer
    permission_classes = [IsAuthenticated]


class UomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Uom.objects.all()
    serializer_class = UomSerializer

    def delete(self, request, pk, format=None):
        uom = Uom.objects.filter(public_id=pk)
        if uom:
            uom.delete()
            return HttpResponse(f'The uom with id: {pk} has been deleted.')
        return HttpResponse(f'The uom with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        uom = Uom.objects.get(public_id=pk)
        if uom:
            serializer = UomSerializer(uom)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        uom = Uom.objects.get(public_id=pk)
        if uom:
            serializer = UomSerializer(uom, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** Good API view *************************************
class GoodListAPIView(generics.ListCreateAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            category_public_id = request.data['category']
            uom_public_id = request.data['basic_uom']
            category = Category.objects.get(public_id=category_public_id)
            uom = Uom.objects.get(public_id=uom_public_id)
            serializer.save(basic_uom=uom, category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer

    def delete(self, request, pk, format=None):
        good = Good.objects.filter(public_id=pk)
        if good:
            good.delete()
            return HttpResponse(f'The uom with id: {pk} has been deleted.')
        return HttpResponse(f'The uom with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        good = Good.objects.get(public_id=pk)
        if good:
            serializer = GoodSerializer(good)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        good = Good.objects.get(public_id=pk)
        if good:
            serializer = GoodSerializer(good, data=request.data)
            uom_public_id = request.data['basic_uom']
            category_public_id = request.data['category']
            if serializer.is_valid():
                category = Category.objects.get(public_id=category_public_id)
                uom = Uom.objects.get(public_id=uom_public_id)
                serializer.save(basic_uom=uom, category=category)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

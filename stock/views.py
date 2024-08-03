from django.http import HttpResponse, JsonResponse
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Warehouse, Category, Uom, Good, StockCard, Document, \
    GoodTransaction, DocumentLine
from .serializers import WarehouseSerializer, CategorySerializer, UomSerializer, \
    GoodSerializer, StockCardSerializer, DocumentSerializer, GoodTransactionSerializer,\
    DocumentLineSerializer
from counterparties.models import Counterparty, Agreement
from .services import post_invoice, unpost_invoice, stock_report


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
            category_public_id = request.data['category_id']
            uom_public_id = request.data['basic_uom_id']
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
            return HttpResponse(f'The good with id: {pk} has been deleted.')
        return HttpResponse(f'The good with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        good = Good.objects.get(public_id=pk)
        if good:
            serializer = GoodSerializer(good)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        good = Good.objects.get(public_id=pk)
        if good:
            serializer = GoodSerializer(good, data=request.data)
            uom_public_id = request.data['basic_uom_id']
            category_public_id = request.data['category_id']
            if serializer.is_valid():
                category = Category.objects.get(public_id=category_public_id)
                uom = Uom.objects.get(public_id=uom_public_id)
                serializer.save(basic_uom=uom, category=category)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** StockCard API view *************************************
class StockCardListAPIView(generics.ListCreateAPIView):
    queryset = StockCard.objects.all()
    serializer_class = StockCardSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = StockCardSerializer(data=request.data)
        if serializer.is_valid():
            warehouse_public_id = request.data['warehouse']
            good_public_id = request.data['good']
            warehouse = Warehouse.objects.get(public_id=warehouse_public_id)
            good = Good.objects.get(public_id=good_public_id)
            serializer.save(good=good, warehouse=warehouse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockCardDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockCard.objects.all()
    serializer_class = StockCardSerializer

    def delete(self, request, pk, format=None):
        stock_card = StockCard.objects.filter(public_id=pk)
        if stock_card:
            stock_card.delete()
            return HttpResponse(f'The stock card with id: {pk} has been deleted.')
        return HttpResponse(f'The stock card with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        stock_card = StockCard.objects.get(public_id=pk)
        if stock_card:
            serializer = StockCardSerializer(stock_card)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        stock_card = StockCard.objects.get(public_id=pk)
        if stock_card:
            serializer = StockCardSerializer(stock_card, data=request.data)
            if serializer.is_valid():
                warehouse_public_id = request.data['warehouse']
                good_public_id = request.data['good']
                warehouse = Warehouse.objects.get(public_id=warehouse_public_id)
                good = Good.objects.get(public_id=good_public_id)
                serializer.save(good=good, warehouse=warehouse)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** Document API view *************************************
class DocumentListAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            counterparty_public_id = request.data['counterparty_id']
            agreement_public_id = request.data['agreement_id']
            counterparty = Counterparty.objects.get(public_id=counterparty_public_id)
            agreement = Agreement.objects.get(public_id=agreement_public_id)
            print(agreement)
            serializer.save(counterparty=counterparty, agreement=agreement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def delete(self, request, pk, format=None):
        document = Document.objects.filter(public_id=pk)
        if document:
            document.delete()
            return HttpResponse(f'The document with id: {pk} has been deleted.')
        return HttpResponse(f'The document with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        document = Document.objects.get(public_id=pk)
        if document:
            serializer = DocumentSerializer(document)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        document = Document.objects.get(public_id=pk)
        if document:
            serializer = DocumentSerializer(document, data=request.data)
            if serializer.is_valid():
                counterparty_id = request.data['counterparty_id']
                agreement_public_id = request.data['agreement_id']
                counterparty = Counterparty.objects.get(public_id=counterparty_id)
                agreement = Agreement.objects.get(public_id=agreement_public_id)
                serializer.save(counterparty=counterparty, agreement=agreement)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** GoodTransaction API view *************************************
class GoodTransactionListAPIView(generics.ListCreateAPIView):
    queryset = GoodTransaction.objects.all()
    serializer_class = GoodTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            document_id = self.request.query_params.get('document_id')
            if document_id:
                return GoodTransaction.objects.filter(document__public_id=document_id)
        except:
            return HttpResponse('There is no such document!')

    def post(self, request, format=None):
        serializer = GoodTransactionSerializer(data=request.data)
        if serializer.is_valid():
            card_public_id = request.data['card']
            document_public_id = request.data['document']
            good_public_id = request.data['good']
            document_line_id = request.data['document_line']
            card = StockCard.objects.get(public_id=card_public_id)
            document = Document.objects.get(public_id=document_public_id)
            good = Good.objects.get(public_id=good_public_id)
            document_line = DocumentLine.objects.get(public_id=document_line_id)
            serializer.save(card=card, document=document, good=good, document_line=document_line)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodTransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GoodTransaction.objects.all()
    serializer_class = GoodTransactionSerializer

    def delete(self, request, pk, format=None):
        if pk:
            good_transaction = GoodTransaction.objects.filter(public_id=pk)
            if good_transaction:
                good_transaction.delete()
                return HttpResponse(f'The good transaction with id: {pk} has been deleted.')
        return HttpResponse(f'The good transaction with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        good_transaction = GoodTransaction.objects.get(public_id=pk)
        if good_transaction:
            serializer = GoodTransactionSerializer(good_transaction)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        good_transaction = GoodTransaction.objects.get(public_id=pk)
        if good_transaction:
            serializer = GoodTransactionSerializer(good_transaction, data=request.data)
            if serializer.is_valid():
                card_public_id = request.data['card']
                document_public_id = request.data['document']
                good_public_id = request.data['good']
                document_line_id = request.data['document_line']
                card = StockCard.objects.get(public_id=card_public_id)
                document = Document.objects.get(public_id=document_public_id)
                good = Good.objects.get(public_id=good_public_id)
                document_line = DocumentLine.objects.get(public_id=document_line_id)
                serializer.save(card=card, document=document, good=good, document_line=document_line)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** DocumentLine API view *************************************
class DocumentLineListAPIView(generics.ListCreateAPIView):
    queryset = DocumentLine.objects.all()
    serializer_class = DocumentLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            document_id = self.request.query_params.get('document_id')
            if document_id:
                return DocumentLine.objects.filter(document__public_id=document_id)
        except:
            return HttpResponse('There is no such document!')

    def post(self, request, format=None):
        serializer = DocumentLineSerializer(data=request.data)
        if serializer.is_valid():
            good_public_id = request.data['good_id']
            document_public_id = request.data['document']
            warehouse_public_id = request.data['warehouse_id']
            good = Good.objects.get(public_id=good_public_id)
            document = Document.objects.get(public_id=document_public_id)
            warehouse = Warehouse.objects.get(public_id=warehouse_public_id)
            serializer.save(good=good, document=document, warehouse=warehouse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentLineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentLine.objects.all()
    serializer_class = DocumentLineSerializer

    def delete(self, request, pk, format=None):
        document_line = DocumentLine.objects.get(public_id=pk)
        if document_line:
            document_line.delete()
            return HttpResponse(f'The document line with id: {pk} has been deleted.')
        return HttpResponse(f'The document line id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        document_line = DocumentLine.objects.get(public_id=pk)
        if document_line:
            serializer = DocumentLineSerializer(document_line)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        document_line = DocumentLine.objects.get(public_id=pk)
        if document_line:
            serializer = DocumentLineSerializer(document_line, data=request.data)
            if serializer.is_valid():
                good_public_id = request.data['good_id']
                document_public_id = request.data['document']
                warehouse_public_id = request.data['warehouse_id']
                good = Good.objects.get(public_id=good_public_id)
                document = Document.objects.get(public_id=document_public_id)
                warehouse = Warehouse.objects.get(public_id=warehouse_public_id)
                serializer.save(good=good, document=document, warehouse=warehouse)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_invoice_view(request):
    return HttpResponse(post_invoice(request))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unpost_invoice_view(request):
    return HttpResponse(unpost_invoice(request))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_report_view(request):
    return HttpResponse(stock_report(request))

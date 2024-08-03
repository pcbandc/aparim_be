from datetime import datetime, time
import pytz
from django.db.models import Sum, Count, When, Case, F, Q
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from .models import StockCard, GoodTransaction, Good
from .serializers import GoodSerializer, StockReportSerializer
from .exceptions import NotEnoughStock
from .models import Document

INFLOW_TRANSACTIONS = ['RT', 'DN', 'MF']
OUTFLOW_TRANSACTIONS = ['DH', 'CN', 'WO', 'MT']


def check_availability(good, warehouse, quantity, time):
    stock_cards = StockCard.objects.filter(
        good=good,
        balance__gt=0,
        time__lt=time,
        warehouse=warehouse
    )
    balance = stock_cards.aggregate(sum=Sum('balance'))['sum']
    return balance - quantity


def fifo(good, warehouse, quantity, document, line):
    left_to_dispatch = quantity
    cards = StockCard.objects.filter(
        good=good,
        balance__gt=0,
        time__lt=document.time,
        warehouse=warehouse
    ).order_by('time')
    balance = cards.aggregate(sum=Sum('balance'))['sum']
    if balance < quantity:
        raise NotEnoughStock(good, warehouse, document.time,
                             quantity - balance)
    for card in cards:
        if card.balance >= left_to_dispatch:
            GoodTransaction.objects.create(
                good=good,
                card=card,
                document=document,
                document_line=line,
                transaction_type='DH',
                quantity=left_to_dispatch,
                cost=card.cost
            )
            card.balance -= left_to_dispatch
            card.save()
            break
        else:
            GoodTransaction.objects.create(
                good=good,
                card=card,
                document=document,
                document_line=line,
                transaction_type='DH',
                quantity=card.balance,
                cost=card.cost
            )
            left_to_dispatch -= card.balance
            card.balance = 0
            card.save()


def post_purchase_invoice(document):
    if document:
        if document.posted:
            return JsonResponse({"data": f'Document # {document.number} dd {document.time} '
                                f'has been already posted'})
        lines = document.lines.all()
        with transaction.atomic():
            for line in lines:
                card = StockCard.objects.create(good=line.good,
                                                time=document.time,
                                                warehouse=line.warehouse,
                                                balance=line.quantity,
                                                cost=line.price)
                GoodTransaction.objects.create(good=line.good,
                                               card=card,
                                               document=document,
                                               document_line=line,
                                               transaction_type='RT',
                                               quantity=line.quantity,
                                               cost=line.price)
            document.posted = True
            document.save()
        return JsonResponse({"data": f'Document # {document.number} dd {document.time} has been '
                            f'successfully posted'})


def unpost_purchase_invoice(document):
    if document:
        if not document.posted:
            return JsonResponse({"error": f'Document # {document.number} dd {document.time} '
                                f'is already unposted'})
        document_transactions = document.transactions.all()
        cards_ids = list(document_transactions.values_list("card", flat=True))
        cards_transactions = GoodTransaction.objects.filter(card__in=cards_ids)
        cards_consumption_transactions = cards_transactions.exclude(transaction_type='RT')
        if len(cards_consumption_transactions) > 0:
            return JsonResponse({"error": f'Forbidden! There are following consumption transactions'
                                          f'recorded on goods received under this document:'})
        with transaction.atomic():
            document_transactions.delete()
            cards = StockCard.objects.filter(id__in=cards_ids)
            cards.delete()
            document.posted = False
            document.save()
        return JsonResponse({"data": f'Document # {document.number} dd {document.time} has been '
                            f'successfully unposted'})


def post_sales_invoice(document):
    if document:
        if document.posted:
            return JsonResponse({"error": f'Document # {document.number} dd {document.time} '
                                f'has been already posted'})
        lines = document.lines.all()
        with transaction.atomic():
            for line in lines:
                fifo(line.good, line.warehouse, line.quantity, document, line)
            document.posted = True
            document.save()
        return JsonResponse({"info": f'Document # {document.number} dd {document.time} has been '
                            f'successfully posted'})


def unpost_sales_invoice(document):
    if document:
        if not document.posted:
            return JsonResponse({"data": f'Document # {document.number} dd {document.time} '
                                f'is already unposted'})
        with transaction.atomic():
            good_transactions = GoodTransaction.objects.filter(document=document)
            for good_transaction in good_transactions:
                card = good_transaction.card
                card.balance += good_transaction.quantity
                card.save()
                good_transaction.delete()
            document.posted = False
            document.save()
        return JsonResponse({"data": f'Document # {document.number} dd {document.time} has been '
                            f'successfully unposted'})


def post_invoice(request):
    try:
        document_id = request.data['document']
        document = Document.objects.get(public_id=document_id)
        if document.type == 'PI':
            return post_purchase_invoice(document)
        if document.type == 'SI':
            return post_sales_invoice(document)
    except NotEnoughStock as e:
        return JsonResponse({"error": e.message})
    except:
        return JsonResponse({"data": "Something went wrong!"})


def unpost_invoice(request):
    try:
        document_id = request.data['document']
        document = Document.objects.get(public_id=document_id)
        if document.type == 'PI':
            return unpost_purchase_invoice(document)
        if document.type == 'SI':
            return unpost_sales_invoice(document)
    except:
        return JsonResponse({"data": "Something went wrong!"})


def stock_report_period_warehouse_category():
    serializer = StockReportSerializer
    start_date = datetime.combine(datetime(2024, 6, 3), time.min, tzinfo=pytz.UTC)
    end_date = datetime.combine(datetime(2024, 6, 5), time.max, tzinfo=pytz.UTC)
    warehouses = [1]
    categories = [4]
    goods = Good.objects.filter(category__in=categories).annotate(
        start_balance_count=Sum(
            Case(
                When(
                    transactions__transaction_type__in=INFLOW_TRANSACTIONS,
                    transactions__document__time__lte=start_date,
                    transactions__card__warehouse__in=warehouses,
                    then='transactions__quantity',
                ),
                When(
                    transactions__transaction_type__in=OUTFLOW_TRANSACTIONS,
                    transactions__document__time__lte=start_date,
                    transactions__card__warehouse__in=warehouses,
                    then=-F('transactions__quantity'),
                ),
            )
        ),
        start_balance_sum=Sum(
            Case(
                When(
                    transactions__transaction_type__in=INFLOW_TRANSACTIONS,
                    transactions__document__time__lte=start_date,
                    transactions__card__warehouse__in=warehouses,
                    then=F('transactions__quantity') * F('transactions__cost'),
                ),
                When(
                    transactions__transaction_type__in=OUTFLOW_TRANSACTIONS,
                    transactions__document__time__lte=start_date,
                    transactions__card__warehouse__in=warehouses,
                    then=-F('transactions__quantity') * F('transactions__cost'),
                ),
            )
        ),
        inflow_total_count=Sum(
            Case(
                When(
                    transactions__transaction_type__in=INFLOW_TRANSACTIONS,
                    transactions__document__time__gte=start_date,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then='transactions__quantity',
                ),
            )
        ),
        inflow_total_sum=Sum(
            Case(
                When(
                    transactions__transaction_type__in=INFLOW_TRANSACTIONS,
                    transactions__document__time__gte=start_date,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then=F('transactions__quantity') * F('transactions__cost'),
                ),
            )
        ),
        outflow_total_count=Sum(
            Case(
                When(
                    transactions__transaction_type__in=['DH'],
                    transactions__document__time__gte=start_date,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then='transactions__quantity',
                ),
            )
        ),
        outflow_total_sum=Sum(
            Case(
                When(
                    transactions__transaction_type__in=['DH'],
                    transactions__document__time__gte=start_date,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then=F('transactions__quantity') * F('transactions__cost'),
                ),
            )
        ),
        end_balance_count=Sum(
            Case(
                When(
                    transactions__transaction_type__in=INFLOW_TRANSACTIONS,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then='transactions__quantity',
                ),
                When(
                    transactions__transaction_type__in=OUTFLOW_TRANSACTIONS,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then=-F('transactions__quantity'),
                ),
            )
        ),
        end_balance_sum=Sum(
            Case(
                When(
                    transactions__transaction_type__in=INFLOW_TRANSACTIONS,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then=F('transactions__quantity') * F('transactions__cost'),
                ),
                When(
                    transactions__transaction_type__in=OUTFLOW_TRANSACTIONS,
                    transactions__document__time__lte=end_date,
                    transactions__card__warehouse__in=warehouses,
                    then=-F('transactions__quantity') * F('transactions__cost'),
                ),
            )
        ),
    )
    return serializer(goods, many=True).data


def stock_report(request):
    return JsonResponse({'report': stock_report_period_warehouse_category()})


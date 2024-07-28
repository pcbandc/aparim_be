from django.db.models import Sum
from django.db import transaction
from django.http import HttpResponse
from .models import StockCard, GoodTransaction
from .exceptions import NotEnoughStock
from .models import Document


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
            return HttpResponse(f'Document # {document.number} dd {document.time} '
                                f'has been already posted')
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
        return HttpResponse(f'Document # {document.number} dd {document.time} has been '
                            f'successfully posted')


def unpost_purchase_invoice(document):
    if document:
        if not document.posted:
            return HttpResponse(f'Document # {document.number} dd {document.time} '
                                f'is already unposted')
        with transaction.atomic():
            document_transactions = GoodTransaction.objects.filter(document=document)
            cards_ids = document_transactions.values_list("card", flat=True)
            cards = StockCard.objects.filter(id__in=cards_ids)
            cards_transactions = GoodTransaction.objects.filter(card__in=cards_ids)
            cards_consumption_transactions = cards_transactions.exclude(transaction_type='RT')
            if len(cards_consumption_transactions) > 0:
                return HttpResponse(f'Forbidden! There are following consumption transactions'
                                    f'recorded on goods received under this document:')
            document_transactions.delete()
            cards.delete()
            document.posted = False
            document.save()
        return HttpResponse(f'Document # {document.number} dd {document.time} has been '
                            f'successfully unposted')


def post_sales_invoice(document):
    if document:
        if document.posted:
            return HttpResponse(f'Document # {document.number} dd {document.time} '
                                f'has been already posted')
        lines = document.lines.all()
        with transaction.atomic():
            for line in lines:
                fifo(line.good, line.warehouse, line.quantity, document, line)
            document.posted = True
            document.save()
        return HttpResponse(f'Document # {document.number} dd {document.time} has been '
                            f'successfully posted')


def unpost_sales_invoice(document):
    if document:
        if not document.posted:
            return HttpResponse(f'Document # {document.number} dd {document.time} '
                                f'is already unposted')
        with transaction.atomic():
            good_transactions = GoodTransaction.objects.filter(document=document)
            for good_transaction in good_transactions:
                card = good_transaction.card
                card.balance += good_transaction.quantity
                card.save()
                good_transaction.delete()
            document.posted = False
            document.save()
        return HttpResponse(f'Document # {document.number} dd {document.time} has been '
                            f'successfully unposted')


def post_invoice(request):
    try:
        document_id = request.data['document']
        document = Document.objects.get(public_id=document_id)
        if document.type == 'PI':
            return post_purchase_invoice(document)
        if document.type == 'SI':
            return post_sales_invoice(document)
    except NotEnoughStock as e:
        return HttpResponse(repr(e))
    except:
        return HttpResponse("Something went wrong!")


def unpost_invoice(request):
    try:
        document_id = request.data['document']
        document = Document.objects.get(public_id=document_id)
        if document.type == 'PI':
            return unpost_purchase_invoice(document)
        if document.type == 'SI':
            return unpost_sales_invoice(document)
    except:
        return HttpResponse("Something went wrong!")




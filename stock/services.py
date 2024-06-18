from django.db.models import Sum
from .models import StockCard, GoodTransaction
from .exceptions import NotEnoughStock


def check_availability(good, warehouse, quantity, time):
    stock_cards = StockCard.objects.filter(
        good=good,
        balance__gt=0,
        time__lt=time,
        warehouse=warehouse
    )
    balance = stock_cards.aggregate(sum=Sum('balance'))['sum']
    return balance - quantity


def fifo(good, warehouse, quantity, document):
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
                transaction_type='DH',
                quantity=card.balance,
                cost=card.cost
            )
            left_to_dispatch -= card.balance
            card.balance = 0
            card.save()




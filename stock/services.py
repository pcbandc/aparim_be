from django.db.models import Sum
from .models import StockCard
from .exceptions import NotEnoughStock


def check_availability(good, warehouse, quantity, time):
    stock_cards = StockCard.objects.filter(good=good, balance__gt=0,
                                           time__lt=time, warehouse=warehouse)
    balance = stock_cards.aggregate(sum=Sum('balance'))['sum']
    return balance - quantity


def fifo(good, warehouse, quantity, time):
    cards = StockCard.objects.filter(good=good, balance__gt=0, time__lt=time,
                                     warehouse=warehouse)\
                             .order_by('time')
    for card in cards:
        print(card.balance)
    balance = cards.aggregate(sum=Sum('balance'))['sum']
    available = balance - quantity
    if available < 0:
        raise NotEnoughStock(good, warehouse, time, -available)


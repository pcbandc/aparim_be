from rest_framework import generics, status
from rest_framework.response import Response
from .models import Counterparty
from .serializers import CounterpartySerializer
from django.http import HttpResponse


class CounterpartyListAPIView(generics.ListCreateAPIView):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer


class CounterpartyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer

    def delete(self, request, pk, format=None):
        counterparty = Counterparty.objects.filter(public_id=pk)
        if counterparty:
            counterparty.delete()
            return HttpResponse(f'The counterparty with id: {pk} has been deleted.')
        return HttpResponse(f'The counterparty with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        counterparty = Counterparty.objects.get(public_id=pk)
        if counterparty:
            serializer = CounterpartySerializer(counterparty)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        counterparty = Counterparty.objects.get(public_id=pk)
        if counterparty:
            serializer = CounterpartySerializer(counterparty, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











from rest_framework import generics, status
from rest_framework.response import Response
from .models import Counterparty, Agreement, ContactPerson, Contact
from .serializers import CounterpartySerializer, AgreementSerializer, ContactPersonSerializer, \
    ContactSerializer
from django.http import HttpResponse


# ***************************** Counterparty API view *************************************
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


# ***************************** Agreement API view *************************************
class AgreementListAPIView(generics.ListCreateAPIView):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer


class AgreementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer

    def delete(self, request, pk, format=None):
        agreement = Agreement.objects.filter(public_id=pk)
        if agreement:
            agreement.delete()
            return HttpResponse(f'The agreement with id: {pk} has been deleted.')
        return HttpResponse(f'The agreement with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        agreement = Agreement.objects.get(public_id=pk)
        if agreement:
            serializer = CounterpartySerializer(agreement)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        agreement = Agreement.objects.get(public_id=pk)
        if agreement:
            serializer = AgreementSerializer(agreement, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** Contact person API view *************************************
class ContactPersonListAPIView(generics.ListCreateAPIView):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer


class ContactPersonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer

    def delete(self, request, pk, format=None):
        contact_person = ContactPerson.objects.filter(public_id=pk)
        if contact_person:
            contact_person.delete()
            return HttpResponse(f'The contact person with id: {pk} has been deleted.')
        return HttpResponse(f'The contact person with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        contact_person = ContactPerson.objects.get(public_id=pk)
        if contact_person:
            serializer = ContactPersonSerializer(contact_person)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        contact_person = ContactPerson.objects.get(public_id=pk)
        if contact_person:
            serializer = ContactPersonSerializer(contact_person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***************************** Contact  API view *************************************
class ContactListAPIView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def delete(self, request, pk, format=None):
        contact = Contact.objects.filter(public_id=pk)
        if contact:
            contact.delete()
            return HttpResponse(f'The contact with id: {pk} has been deleted.')
        return HttpResponse(f'The contact with id: {pk} does not exist in the database.')

    def get(self, request, pk, format=None):
        contact = Contact.objects.get(public_id=pk)
        if contact:
            serializer = ContactPersonSerializer(contact)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        contact = Contact.objects.get(public_id=pk)
        if contact:
            serializer = ContactPersonSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








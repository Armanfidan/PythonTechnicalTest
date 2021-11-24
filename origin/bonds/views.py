import requests
from django.core.exceptions import FieldError
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import BondSerializer
from .models import Bond
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import logging


class BondView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_bonds = Bond.objects.filter(user=request.user)
        serializer = BondSerializer(all_bonds, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if 'legal_name' not in request.data:
            response = requests.get(url='https://api.gleif.org/api/v1/lei-records/' + request.data['lei'], timeout=5)
            if response.status_code == 200:
                request.data['legal_name'] = response.json()['data']['attributes']['entity']['legalName']['name']
            else:
                raise FieldError('Legal name could not be acquired from LEI. Please check your fields.')
        serializer = BondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

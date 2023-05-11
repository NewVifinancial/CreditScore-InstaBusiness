

# # Create your views here.
# create views for Transactions, Calculation, CreditScore


from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import TransactionsSerializer, CalculationSerializer, CreditScoreSerializer
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from .models import Transactions , Calculation, CreditScore



class TransactionsAPIView(views.APIView):
   
    serializer_class = TransactionsSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = TransactionsSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

    def get(self,request):
        transaction_ = Transactions.objects.all()
    
        transaction_serializer = TransactionsSerializer(transaction_, many=True)
        return JsonResponse(transaction_serializer.data, safe=False)
        # 'safe=False' for objects serialization    

@api_view(['GET'])
def transactionRetrieveAPIview(request,id_num):

    transaction_ = get_object_or_404(CreditScore,id_number=id_num)
    
    transaction_serializer = TransactionsSerializer(transaction_)
    return JsonResponse(transaction_serializer.data, safe=False)
    # 'safe=False' for objects serialization

class CalculationAPIView(views.APIView):
    
    serializer_class = CalculationSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = CalculationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

    def get(self,request):
        calculation_ = CreditScore.objects.all()
    
        calculation_serializer = CreditScoreSerializer(calculation_, many=True)
        return JsonResponse(calculation_serializer.data, safe=False)
        # 'safe=False' for objects serialization      

@api_view(['GET'])
def calculationRetrieveAPIview(request,id_num):

    calculation_ = get_object_or_404(CreditScore,id_number=id_num)
    
    calculation_serializer = CalculationSerializer(calculation_)
    return JsonResponse(calculation_serializer.data, safe=False)
    # 'safe=False' for objects serialization

 
class CreditScoreAPIView(views.APIView):
    """
    A simple APIView for creating creditscore entires.
    """
    serializer_class = CreditScoreSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = CreditScoreSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
    
    def get(self,request):
        creditscore_ = CreditScore.objects.all()
    
        creditscore_serializer = CreditScoreSerializer(creditscore_, many=True)
        return JsonResponse(creditscore_serializer.data, safe=False)
        # 'safe=False' for objects serialization

     
    
        
@api_view(['GET'])
def creditScoreRetrieveAPIview(request,id_num):

    creditscore_ = get_object_or_404(CreditScore,id_number=id_num)
    
    creditscore_serializer = CreditScoreSerializer(creditscore_)
    return JsonResponse(creditscore_serializer.data, safe=False)
    # 'safe=False' for objects serialization

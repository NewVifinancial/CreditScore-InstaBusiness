from . import models
from rest_framework_json_api import serializers
from rest_framework import serializers
import rest_framework.fields


class TransactionsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Transactions
		fields = "__all__"
	

	
class CalculationSerializer(serializers.ModelSerializer):

	
	class Meta:
			model = models.Calculation
			fields = "__all__"
		
	

class CreditScoreSerializer(serializers.ModelSerializer):
   
    
	class Meta:
		model = models.CreditScore
		fields = "__all__"
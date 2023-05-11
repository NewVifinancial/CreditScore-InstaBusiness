from django.contrib import admin
from .models import Transactions, Calculation, CreditScore

# Register your models here.

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_name')

admin.site.register(Calculation)
admin.site.register(CreditScore)
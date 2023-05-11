from django.db import models

# # Create your models here.



class Transactions(models.Model):
    transaction_date = models.DateField('Transaction Date',blank=True,null=True)
    transaction_time =models.TimeField('Transaction Time')
    from_acct = models.IntegerField('Sending Account ID')
    from_name = models.CharField('Sending AccountName', max_length=50)
    from_no = models.IntegerField('Sending Phone Number')
    trans_type = models.CharField('Transaction Type', max_length=50)
    amount = models.DecimalField('Amount',decimal_places=2,max_digits=15)
    fees = models.DecimalField('Fees',decimal_places=2,max_digits=15)
    ba_before = models.DecimalField('Balance Before',decimal_places=2,max_digits=15)
    bal_after = models.DecimalField('Balance After',decimal_places=2,max_digits=15)
    to_no = models.IntegerField('Receiving PhoneNumber')
    to_name = models.CharField('Receiving AccountName', max_length=50)
    to_acct = models.CharField('Receiving PhoneNumber',blank=True,max_length=50)
    f_id = models.CharField('Transaction ID',max_length=255)
    ref = models.CharField('Reference',blank=True, max_length=50)
    ova = models.CharField('Online Vendor Account', max_length=50)

    
    # def __str__(self):
    #     return f'{self.title}'
    
    # def __str__(self):
    #     return '{} - {}{}{}{}'(self.transaction_date)
    #     return self.from_name


class Calculation(models.Model):

    freq_activity = models.IntegerField()
    freq_of_rebal = models.IntegerField()
    mode_cash_in = models.IntegerField() # month with highestcash in transactions
    median_cash_in = models.IntegerField() # median cash In transactions per month
    mode_cash_out = models.IntegerField() # month with highest cash out transactions
    median_cash_out = models.IntegerField() # median cash Out transactions per month

 
    

class CreditScore(models.Model):
    
    id_number =models.IntegerField(unique=True)
    agent_name = models.CharField('Agent Name',null=True,blank=True, max_length=255)
    len_of_serve_score = models.IntegerField(blank=True,null=True)
    freq_act_score = models.IntegerField(blank=True,null=True)
    freq_rebal_score = models.IntegerField(blank=True,null=True)
    mode_cash_in_score = models.IntegerField(blank=True,null=True) # month with highestcash in transactions
    median_cash_in_score = models.IntegerField(blank=True,null=True) # median cash In transactions per month
    mode_cash_out_score = models.IntegerField(blank=True,null=True) # month with highest cash out transactions
    median_cash_out_score = models.IntegerField(blank=True,null=True) # median cash Out transactions per month
    credit_score = models.IntegerField(blank=True,null=True)
    eligibility = models.IntegerField(blank=True,null=True)
    freq_activity = models.IntegerField(blank=True,null=True)
    freq_of_rebal = models.IntegerField(blank=True,null=True)
    mode_cash_in = models.IntegerField(blank=True,null=True) # month with highestcash in transactions
    median_cash_in = models.IntegerField(blank=True,null=True) # median cash In transactions per month
    mode_cash_out = models.IntegerField(blank=True,null=True) # month with highest cash out transactions
    median_cash_out = models.IntegerField(blank=True,null=True) # median cash Out transactions per month

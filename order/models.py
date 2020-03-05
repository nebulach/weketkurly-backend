from django.db import models

class CreditCard(models.Model):
    card_name           = models.CharField(max_length = 10)
    card_description    = models.CharField(max_length = 200, blank = True, null = True)
    card_point          = models.CharField(max_length = 100, blank = True, null = True)
    card_discount_event = models.CharField(max_length = 100, blank = True, null = True)
    
    class Meta :
        db_table = 'creditcards'

class InstallmentPeriod(models.Model):
    credit_card         = models.ManyToManyField(CreditCard)
    installment_period  = models.CharField(max_length = 10)  
    
    class Meta :
        db_table = 'installmentPeriod'
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


class Cart(models.Model) :
    user        = models.ForeignKey('users.User', on_delete = models.SET_NULL, null = True) 
    created_at  = models.DateTimeField(auto_now_add = True)
    
    class Meta :
        db_table = 'carts'


class CartDetail(models.Model) :
    cart        = models.ForeignKey('Cart', on_delete = models.SET_NULL, blank = True, null = True)
    products    = models.ForeignKey('products.Product', on_delete = models.SET_NULL, blank = True, null = True)
    quantity    = models.IntegerField(default = 1)
    
    class Meta :
        db_table = 'cartdetails'


class Order(models.Model) :
    cart                = models.ForeignKey('Cart', on_delete = models.SET_NULL, blank = True, null = True)
    user                = models.ForeignKey('users.User', on_delete = models.SET_NULL, blank = True, null = True)
    address             = models.ForeignKey('users.Address', on_delete = models.SET_NULL, blank = True, null = True)
    receiver_name       = models.CharField(max_length = 20, blank = True, null = True)
    receiver_phone      = models.CharField(max_length = 20, blank = True, null = True)  
    delivery_request    = models.CharField(max_length = 60, blank = True, null = True)
    created_at          = models.DateTimeField(auto_now_add=True)
    order_number        = models.CharField(max_length = 20, unique = True, blank = True, null = True)
    
    class Meta :
        db_table = 'orders'


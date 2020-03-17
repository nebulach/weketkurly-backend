import json

from .models import CreditCard, InstallmentPeriod

from django.views import View
from django.http import JsonResponse 

class CreditCardView(View):
    def get(self, request):
        credit_list = [
            {   
                'card_name'             : card.card_name,
                'card_description'      : card.card_description,
                'card_point'            : card.card_point,
                'card_discount_event'   : card.card_discount_event,
                'installment_perioid'   : [
                    install['installment_period']  
                for install in card.installmentperiod_set.values()] 
            }
            for card in CreditCard.objects.all()
        ]

        return JsonResponse({"data" : list(credit_list)}, status = 200)

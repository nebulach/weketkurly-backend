from django.urls    import path
from .views         import CreditCardView, CartView, OrderView, AddressView

urlpatterns = [
    path('/card', CreditCardView.as_view()),
    path('/cart', CartView.as_view()),
    path('', OrderView.as_view())
]

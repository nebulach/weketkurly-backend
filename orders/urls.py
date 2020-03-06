from django.urls    import path
from .views         import CreditCardView

urlpatterns = [
    path('/card', CreditCardView.as_view()),
]

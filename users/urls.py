from django.urls    import path
from .views         import SignInView, SignUpView, CheckAccountView, CheckEmailView

urlpatterns = [
    path('/sign-in', SignInView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/check-account', CheckAccountView.as_view()),
    path('/check-email', CheckEmailView.as_view())
]

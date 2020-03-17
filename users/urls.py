from django.urls    import path
from .views         import SignInView, SignUpView, CheckAccountView, CheckEmailView

urlpatterns = [
    path('/sign-in', SignInView.as_view()),
    path('', SignUpView.as_view()),
    path('/validation', CheckAccountView.as_view()),
    path('/check-email', CheckEmailView.as_view())
]

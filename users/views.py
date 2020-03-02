import json
import bcrypt
import jwt

from .models                        import User, Gender, Grade, Address
from .utils                         import login_required

from WeketKurly_backend.settings    import SECRET_KEY, ALGORITHM
from django.views                   import View
from django.http                    import HttpResponse, JsonResponse
from django.db                      import transaction

# Create your views here.
class SignInView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:
            if User.objects.filter(account=user_data['account']).exists():
                account = User.objects.get(account=user_data['account'])

                if bcrypt.checkpw(user_data['password'].encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'account_id' : account.id}, SECRET_KEY, algorithm=ALGORITHM)
                    
                    return JsonResponse({'token': token.decode('utf-8')}, status=200)
                
                return HttpResponse(status=401)

            return HttpResponse(status=400)
        
        except KeyError:
            return HttpResponse(status=400)



class SignUpView(View):
    def check_capital_area(self, area):
        for capital in ['서울', '경기', '인천']:
            if capital in area:
                return True
        return False

    def post(self, request):
        user_data = json.loads(request.body)
        
        with transaction.atomic():
            try:
                if User.objects.filter(account=user_data['account']).exists():
                    return HttpResponse(status=401)
                
                password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())

                user_model = User(
                    account=user_data['account'],
                    grade=Grade.objects.get(id=1),
                    password=password.decode(),
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    gender=Gender.objects.get(name=user_data['gender']),
                    birthday=user_data['birthday']
                )

                user_model.save()

                # capital area check
                Address(
                    user=User.objects.get(id=user_model.id),
                    address=user_data['address'],
                    is_capital_area=self.check_capital_area(user_data['address'])
                ).save()

                return HttpResponse(status=200)
            
            except KeyError:
                return HttpResponse(status=400)



class CheckAccountView(View):
    def post(self, request):
        user_account = json.loads(request.body)

        if User.objects.filter(account=user_account).exists():
            return JsonResponse({'message': 'INVALID_ID'}, status=400)
        else:
            return HttpResponse(status=200)

class CheckEmailView(View):
    def post(self, request):
        user_email = json.loads(request.body)

        if User.objects.filter(email=user_email).exists():
            return JsonResponse({'message': 'INVALID_ID'}, status=400)
        else:
            return HttpResponse(status=200)


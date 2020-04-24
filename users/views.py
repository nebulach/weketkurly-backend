import json
import bcrypt
import jwt
import re

from .models                        import User, Gender, Grade, Address
from orders.models                  import Cart
from .utils                         import user_authentication

from WeketKurly_backend.settings    import SECRET_KEY, ALGORITHM
from django.views                   import View
from django.http                    import HttpResponse, JsonResponse
from django.db                      import transaction
from django.core.validators         import validate_email
from django.core.exceptions         import ValidationError

ID_VALID    = r'^(?=.*[a-z])[a-z0-9]{6,16}$'
EMAIL_VALID = r'^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z\-]+$'

class SignInView(View):
    def post(self, request):
        user_data = json.loads(request.body)
        try:
            if User.objects.filter(account = user_data['account']).exists():
                account = User.objects.get(account = user_data['account'])

                if bcrypt.checkpw(user_data['password'].encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'account_id' : account.id}, SECRET_KEY, algorithm = ALGORITHM)
                    
                    return JsonResponse({'token': token.decode('utf-8')}, status = 200)
                
                return HttpResponse(status = 401)

            return HttpResponse(status = 401)
        
        except KeyError:
            return HttpResponse(status = 400) 


class SignUpView(View):
    def check_capital_area(self, area):
        for capital in ['서울', '경기', '인천']:
            if capital in area:
                return True
        return False

    def invalid_password(self, password):
        pattern1 = r"^(?=.*[\d])(?=.*[A-Za-z])(?=.*[!@#$%^&*()_+={}?:~\[\]])[A-Za-z\d!@#$%^&*()_+={}?:~\[\]]{10,}$"
        pattern2 = r"^(?=.*[\d])(?=.*[A-Za-z])[A-Za-z\d]{10,}$"
        pattern3 = r"^(?=.*[\d])(?=.*[!@#$%^&*()_+={}?:~\[\]])[\d!@#$%^&*()_+={}?:~\[\]]{10,}$"
        pattern4 = r"^(?=.*[A-Za-z])(?=.*[!@#$%^&*()_+={}?:~\[\]])[A-Za-z!@#$%^&*()_+={}?:~\[\]]{10,}$"

        if re.match(pattern1, password) or re.match(pattern2, password) or re.match(pattern3, password) \
            or re.match(pattern4, password):
            if re.search(r"^(\d)(\1{2})", password):
                return True
            return False
        
        return True

    def invalid_account(self, account):
        pattern1 = r"^(?=.*[\d])(?=.*[A-Za-z])[A-Za-z\d]{6,}$"
        pattern2 = r"^(?=.*[A-Za-z])[A-Za-z]{6,}$"

        if re.match(pattern1, account) or re.match(pattern2, account):
            return False
        return True

    def invalid_phone(self, phone):
        if re.match(r"^\d{3}?\d{4}?\d{4}$", phone):
            return False
        return True

    def post(self, request):
        user_data = json.loads(request.body)
        try:
            if User.objects.filter(account = user_data['account']).exists():
                return HttpResponse(status = 400)

            if self.invalid_account(user_data['account']):
                return HttpResponse(status = 400)

            validate_email(user_data['email'])

            if self.invalid_password(user_data['password']):
                return HttpResponse(status = 400)

            if self.invalid_phone(user_data['phone']):
                return HttpResponse(status = 400)
            
            if user_data['name'] is None:
                return HttpResponse(status = 400)

            with transaction.atomic():
                password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())

                user_model = User(
                    account     = user_data['account'],
                    grade       = Grade.objects.get(id = 1),
                    password    = password,
                    name        = user_data['name'],
                    email       = user_data['email'],
                    phone       = user_data['phone'],
                    gender      = Gender.objects.get(name = user_data['gender']),
                    birth       = user_data['birthday']
                )

                user_model.save()

                Address(
                    user            = User.objects.get(id = user_model.id),
                    address         = user_data['address'],
                    is_capital_area = self.check_capital_area(user_data['address'])
                ).save()

                Cart(
                    user            = User.objects.get(id = user_model.id)
                ).save()
                
                return JsonResponse({"data" : 
                    {   'account'   : user_data['account'],
                        'name'      : user_data['name'],
                        'email'     : user_data['email']}
                        }, status = 200)
        
        except KeyError:
            return HttpResponse(status = 400)

        except ValidationError:
            return HttpResponse(status = 400)


class CheckAccountView(View):
    def post(self, request):
        data = json.loads(request.body)

        if User.objects.filter(account = data['account']).exists():
            return JsonResponse({'message': 'EXISTING_ID'}, status = 400)
        
        if not re.match(ID_VALID, data['account']) :
            return JsonResponse({'message' : 'INVALID_ID'}, status = 400)
        
        return HttpResponse(status = 200)
        
        
class CheckEmailView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if User.objects.filter(email = data['email']).exists():
            return JsonResponse({'message': 'EXISTING_EMAIL'}, status = 400)
        
        if not re.match(EMAIL_VALID, data['email']) :
            return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
        
        return HttpResponse(status = 200)


class MyPageView(View) :
    @user_authentication
    def get(self, request) :
        try : 
            user = request.user
            user_information = {       
                'name'       : user.name,
                'grade'      : user.grade.name,
                'grade_info' : user.grade.info,  
                'phone'      : user.phone,
                'email'      : user.email
            }
            return JsonResponse(user_information, status = 200)
        
        except user.DoesNotExist :
            return JsonResponse({"message":"INVALID_USER"}, status=400)
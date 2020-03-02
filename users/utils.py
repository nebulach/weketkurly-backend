import jwt
import json

from .models                        import User
from WeketKurly_backend.settings    import SECRET_KEY

from django.http                    import JsonResponse

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)

        if token is None:
            return JsonResponse({'message' : "LOGIN_REQUIRED"}, status=401)
        else:
            try:
                decode          = jwt.decode(token, SECRET_KEY, algorithm='HS256')
                user_id         = decode.get('account_id', None)
                user            = User.objects.get(id=account_id)
                request.user    = user

                return func(self, request, *args, **kwargs)
            except jwt.DecodeError:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'message' : 'ACCOUNT_NOT_EXIST'}, status=400)
    
    return wrapper

import json

from .models                import CreditCard, InstallmentPeriod, Cart, CartDetail, Order
from products.models        import Product
from users.models           import User, Address
from users.utils            import user_authentication

from django.views           import View
from django.http            import HttpResponse, JsonResponse 
from django.db.models       import Sum


class CreditCardView(View):
    def get(self, request):
        credit_list = [
            {   
                'card_name'             : card.card_name,
                'card_description'      : card.card_description,
                'card_point'            : card.card_point,
                'card_discount_event'   : card.card_discount_event,
                'installment_perioid'   :   [
                                            install['installment_period']  
                                            for install in card.installmentperiod_set.values()
                                            ] 
            }
            for card in CreditCard.objects.all()
        ]
        
        return JsonResponse({"data" : list(credit_list)}, status = 200)
    
    
class CartView(View) :
    @user_authentication
    def post(self, request) :
        try : 
            data        = json.loads(request.body)
            cart        = Cart.objects.filter(user_id = request.user.id).last()
            cartdetail  = CartDetail.objects.filter(cart_id = cart.id, products_id = data['product_num'])

            if cartdetail.exists(): 
                cartdetail.update(
                    quantity = data['quantity']
                )
                
                return HttpResponse(status=200)
                
            else :
                CartDetail(
                    cart_id           = cart.id,
                    products_id       = data['product_num'],
                    quantity          = data['quantity']
                ).save()
                
                return HttpResponse(status=200)
        
        except KeyError :
            return HttpResponse(status=400) 
        
    @user_authentication
    def get(self, request) :
        cart        = Cart.objects.filter(user_id = request.user.id).last()
        carts       = Cart.objects.prefetch_related('cartdetail_set').get(id = cart.id).cartdetail_set.all()
        
        data = [
            {
                "product_num"           : cart.products_id,
                "name"                  : Product.objects.get(id = cart.products_id).name,
                "original_price"        : Product.objects.get(id = cart.products_id).original_price,
                "discounted_price"      : int(Product.objects.get(id = cart.products_id).original_price * (100 - int(Product.objects.get(id = cart.products_id).discount_percent)) / 100),
                "ea"                    : cart.quantity,
                "min_ea"                : 1,
                "max_ea"                : 999,
                "thumbnail_image_url"   : Product.objects.get(id = cart.products_id).cart_image_url
            }
            for cart in carts
                ]
        
        return JsonResponse({'data' : list(data)}, status = 200)
    
    @user_authentication
    def delete(self, request) :  
        data    = json.loads(request.body)
        cart_id = Cart.objects.filter(user_id = request.user.id).last().id
        
        CartDetail.objects.filter(cart_id = cart_id, products_id = data['product_num']).delete()    

        return HttpResponse(status = 200)


class OrderView(View) :
    ID_OFFSET = 10147747
    
    def check_capital_area(self, area):
        for capital in ['서울', '경기', '인천']:
            if capital in area:
                return True
        return False
    
    @user_authentication
    def post(self, request) :
        try : 
            data            = json.loads(request.body)
            cart            = Cart.objects.filter(user_id = request.user.id).last()
            order_number    = self.ID_OFFSET + Order.objects.latest('id').id
            
            if data['new_address'] == "True" : 
                if Address.objects.filter(user_id = request.user.id, address = data['address']).exists() :
                    receiver_address = Address.objects.filter(user_id = request.user.id, address = data['address']).id
                    
                else :
                    user_address = Address (
                        user_id         = request.user.id,
                        address         = data['address'],
                        is_capital_area = self.check_capital_area(data['address'])
                    )
                    user_address.save()
                    receiver_address = user_address.id
                    
            else :
                receiver_address = data['address']
                
            Order(
                user_id             = request.user.id,
                cart_id             = cart.id,
                receiver_name       = data['receiver_name'],
                receiver_phone      = data['receiver_phone'],
                delivery_request    = data['delivery_request'],
                order_number        = order_number,
                address_id          = receiver_address
            ).save()
        
            Cart(
                user                = User.objects.get(id = request.user.id)
            ).save()
            
            return HttpResponse(status = 200)
            
        except KeyError :
            return HttpResponse(status = 400) 
        
    @user_authentication
    def get(self, request) : 
        orders = Order.objects.filter(user_id = request.user)
        
        def products(num) : 
            product = [
                {
                    'name'                  : cart.products.name,          
                    'ea'                    : cart.quantity,                
                    'original_price'        : cart.products.original_price,  
                    'discounted_price'      : int(Product.objects.get(id = cart.products_id).original_price * (100 - int(Product.objects.get(id = cart.products_id).discount_percent)) / 100),
                    'thumbnail_image_url'   : cart.products.cart_image_url
                }
                for cart in CartDetail.objects.select_related('products').filter(cart_id = num)
            ]
            return product
        
        data = [
            {
                "order_number"  : order.order_number,
                "created_at"    : order.created_at,
                "product"       : products(order.cart_id)
            }
            for order in orders
        ]
        return JsonResponse({'data' : list(data)}, status = 200)
        


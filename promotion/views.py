
from django.shortcuts   import render
from django.views       import View
from django.http        import HttpResponse, JsonResponse 

from .models            import Notice, Event, Recipe
from products.models    import *

def sticker_image_url(discount) :
    if int(discount) == 0 :
        return ""
    
    else :
        return f'https://img-cf.kurly.com/shop/data/my_icon/icon_save_{int(discount)}.png'
    
    
class RecommendationView(View) :
    def get(self, request) :
        banners =   {
                    "banners" : list(Notice.objects.all().values('id', 'banner_image'))
                    }
        
        recommendation_product = [
            {
                'no'                : product.id,
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent)    
            }
            
            for product in Product.objects.order_by('?')[:8]
        ]
        
        recommendation =    {
                                "title"     : "이 상품 어때요?",
                                "products"  : recommendation_product
                            }
        
        events         = list(Event.objects.all().values('id', 'title', 'subtitle', 'image'))
        
        event = {
                    "title"     : "이벤트 소식",
                    "events"    : events
                }
        
        discount_product = [
            {
                'no'                : product.id,
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent)  
            }
            
            for product in Product.objects.exclude(discount_percent = 0).order_by('?')[:6]
        ]
        
        discount =  {
                        "title"     : "알뜰 상품",
                        "products"  : discount_product
                    }
        
        md = {
                "title"         : "MD의 추천",
                "categories"    : list(MainCategory.objects.all().values('id', 'name')[0:15])
            }
                
        new_product = [
            {
                'no'                : product.id,
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent) 
            }
            
            for product in Product.objects.order_by('-incoming_date')[:6]
        ]
        
        new = {
            "title"     : "오늘의 신상품",
            "subtitle"  : "매일 정오, 컬리의 새로운 상품을 만나보세요",
            "products"  : new_product
        }
        
        hot_product = [
            {
                'no'                : product.id,
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent) 
            }
            
            for product in Product.objects.order_by('-sales_index')[:6]
        ]
        
        hot =   {
                    "title"     : "지금 가장 핫한 상품",
                    "products"  : hot_product
                }
        
        sale_product = [
            {
                'no'                : product.id,
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent)  
            }
            
            for product in Product.objects.exclude(discount_percent = 0).order_by('?')[:6]
        ]
        
        sale =  {
                    "title"     : "마감세일",
                    "products"  : sale_product
                }
        
        less_than_3000_product = [
            {
                'no'                : product.id,
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent)  
            }
            
            for product in Product.objects.all().filter(original_price__lte = 3000).order_by('?')[:6]
        ]
        
        less_than_3000 =    {
                                "title": "3천원의 행복",
                                "products" : less_than_3000_product
                            }
        
        recipes =   {
                        "title"     : "컬리의 레시피",
                        "recipes"   : list(Recipe.objects.all().values('id', 'title', 'image'))
                    }
        
        articles = [
                        banners, 
                        recommendation, 
                        event, 
                        discount, 
                        md, 
                        new, 
                        hot, 
                        sale, 
                        less_than_3000, 
                        recipes
                    ]
        
        data =  {
                "section_list" : articles
                }
        
        return JsonResponse({'data' : data}, status = 200)
        
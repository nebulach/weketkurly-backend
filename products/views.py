import json

from .models            import MainCategory, SubCategory, Product, DetailInfomation

from django.views       import View
from django.http        import HttpResponse, JsonResponse 


class CategoryView(View) :
    def get(self, request) :
        category = [
            {
                'main_id'               : main.id,
                'main_category'         : main.name,
                'icon_black_url'        : main.icon_black_url,
                'icon_active_url'       : main.icon_active_url,
                'subcategory'           : list(main.subcategory_set.values('id', 'name', 'thumbnail_url'))
            }
            for main in MainCategory.objects.all().prefetch_related('subcategory_set')
        ]
        return JsonResponse({"data" : category}, status = 200)


class SubCategoryView(View) :
    def get(self, request, main_id) :
        category = [
            {
                'no'        : category.id,
                'name'      : category.name
            }
            for category in SubCategory.objects.filter(maincategory_id = main_id)
        ]
        
        root_category = {
            'main_id'        : main_id,
            'name'           : MainCategory.objects.get(id = main_id).name,
            'categories'     : list(category)
        }
        
        data = {
            'root_category'  : root_category
        }
        
        return JsonResponse({'data' : data}, status = 200)


def sticker_image_url(discount) :
    if int(discount) == 0 :
        return ""
    
    else :
        return f'https://img-cf.kurly.com/shop/data/my_icon/icon_save_{int(discount)}.png'
        
        
class ProductListView(View) :
    def get(self, request, sub_id) :
        products = [
            {
                'name'              : product.name,
                'original_price'    : product.original_price,
                'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'shortdesc'         : product.short_description,
                'list_image_url'    : product.list_image_url,
                'sticker_image_url' : sticker_image_url(product.discount_percent)               
            }
            for product in Product.objects.filter(sub_category_id = sub_id)
        ]
        
        data = {
            'category_name'         : SubCategory.objects.get(id = sub_id).name,
            'products'              : products
        }
        
        paging = {
            'total'                 : Product.objects.filter(sub_category_id = sub_id).count(),
            'next_page_no'          : 2 #페이지네이션 구현
        }
        return JsonResponse({'data' : data, 'paging' : paging}, status = 200)


class DetailView(View) :
    def get(self, request, product_id) :
        product = Product.objects.get(id = product_id)
        data = {
                'no'                        : product.id,
                'name'                      : product.name,
                'short_description'         : product.short_description,
                'unit_text'                 : product.unit_text,
                'weight'                    : product.weight,
                'origin'                    : product.origin,
                'contactant'                : product.contactant,
                'expiration_date'           : product.expiration_date,
                'delivery_time_type_text'   : product.delivery_time_type_text,
                'packing_type_text'         : product.packing_type_text,
                'original_price'            : product.original_price,
                'discounted_price'          : int(product.original_price * (100 - int(product.discount_percent)) / 100),
                'discount_percent'          : int(product.discount_percent),
                'detail_image_url'          : product.detail_image_url,
                'product_description'       : DetailInfomation.objects.get(product_id = product_id).product_description,
                'product_image'             : DetailInfomation.objects.get(product_id = product_id).product_image,
                'product_information'       : DetailInfomation.objects.get(product_id = product_id).product_infomation
                }
        return JsonResponse({'data' : data}, status = 200)
    
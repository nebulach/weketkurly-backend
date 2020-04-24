import json

from .models                import MainCategory, SubCategory, Product, DetailInfomation

from django.views           import View
from django.http            import HttpResponse, JsonResponse 
from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger
from django.db.models       import Q


def sorting(product_list, sort) :
    if sort == '1' :
        product_list = product_list.order_by('-sales_index')
    
    elif sort == '2' :
        product_list = product_list.order_by('original_price')
        
    elif sort == '3' :
        product_list = product_list.order_by('-original_price')
    
    else :
        product_list = product_list.order_by('-incoming_date')
            
    paginator    = Paginator(product_list, 99)    
    
    return paginator    
    

def product_info(contacts) :
    products = [
        {
            'name'              : product.name,
            'original_price'    : product.original_price,
            'price'             : int(product.original_price * (100 - int(product.discount_percent)) / 100),
            'shortdesc'         : product.short_description,
            'list_image_url'    : product.list_image_url,
            'sticker_image_url' : sticker_image_url(product.discount_percent)               
        }
        for product in contacts
    ]
            
    return products


def sticker_image_url(discount) :
    if int(discount) == 0 :
        return ""
    
    else :
        return f'https://img-cf.kurly.com/shop/data/my_icon/icon_save_{int(discount)}.png'
    
    
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
            'no'             : main_id,
            'name'           : MainCategory.objects.get(id = main_id).name,
            'categories'     : list(category)
        }
        
        data = {
            'root_category'  : root_category
        }
        
        return JsonResponse({'data' : data}, status = 200)
        
        
class ProductListView(View) :
    def get(self, request, sub_id) :
        viewPage     = request.GET.get('viewPage', None)
        sort         = request.GET.get('sort_type', None)
        
        product_list = Product.objects.filter(sub_category_id = sub_id)
        
        paginator = sorting(product_list, sort)
                
        try:
            contacts = paginator.page(viewPage)
            
        except PageNotAnInteger:
            contacts = paginator.page(1)  
        
        except EmptyPage:
            return HttpResponse(status = 400) 
        
        products = product_info(contacts)
        
        data = {
            'category_no'           : sub_id,
            'category_name'         : SubCategory.objects.get(id = sub_id).name,
            'products'              : products
        }
        
        paging = {
            'total'                 : product_list.count(),
            'total_page_no'         : paginator.num_pages
        }
        return JsonResponse({'data' : data, 'paging' : paging}, status = 200)


class ProductTotalListView(View) :
    def get(self, request, main_id) :
        viewPage     = request.GET.get('viewPage', None)
        sort         = request.GET.get('sort_type', None)

        total_sub       = MainCategory.objects.prefetch_related('subcategory_set').get(id = main_id).subcategory_set.count()
        product_list    = MainCategory.objects.prefetch_related('subcategory_set').get(id = main_id).subcategory_set.prefetch_related('product_set')[0].product_set.all()
        
        for i in range(1, total_sub) :
            b               = MainCategory.objects.prefetch_related('subcategory_set').get(id = main_id).subcategory_set.prefetch_related('product_set')[i].product_set.all()
            product_list    = product_list.union(b)
            
        paginator = sorting(product_list, sort)
        
        try:
            contacts = paginator.page(viewPage)
            
        except PageNotAnInteger:
            contacts = paginator.page(1)   
        
        except EmptyPage:
            return HttpResponse(status = 400) 
        
        products = product_info(contacts)
        
        data = {
            'category_name'         : MainCategory.objects.get(id = main_id).name,
            'products'              : products
        }
        
        paging = {
            'total'                 : product_list.count(),
            'total_page_no'         : paginator.num_pages
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
    
    
class SearchView(View) : 
    def get(self, request) :
        keyword      = request.GET.get('keyword', None)
        viewPage     = request.GET.get('viewPage', None)
        
        product_search = Product.objects.filter(  Q(name__icontains = keyword) | 
                                                Q(short_description__icontains = keyword) 
                                                ).all()
        
        detail_search = DetailInfomation.objects.filter(Q (product_description__icontains = keyword) |
                                                        Q (product_infomation__icontains = keyword)
                                                        ).select_related('product')
        
        
        paginator    = Paginator(product_search, 99)
        
        try:
            contacts = paginator.page(viewPage)
            
        except PageNotAnInteger:
            contacts = paginator.page(1)   
        
        except EmptyPage:
            return HttpResponse(status = 400)  
        
        products = product_info(contacts)
        
        data = {
            'products'              : products
        }
        
        paging = {
            'total'                 : product_search.count(),
            'total_page_no'         : paginator.num_pages
        }
        return JsonResponse({'data' : data, 'paging' : paging}, status = 200)
    
    
class NewView(View) : 
    def get(self, request) :
        viewPage     = request.GET.get('viewPage', None)
        sort         = request.GET.get('sort_type', None)
        
        product_list = Product.objects.filter(incoming_date__year = 2020)

        paginator = sorting(product_list, sort)
        
        try:
            contacts = paginator.page(viewPage)
            
        except PageNotAnInteger:
            contacts = paginator.page(1)   
        
        except EmptyPage:
            return HttpResponse(status = 400) 
        
        products = product_info(contacts)
        
        data = {
            'category_name'         : '신상품',
            'products'              : products
        }
        
        paging = {
            'total'                 : product_list.count(),
            'total_page_no'         : paginator.num_pages
        }
        return JsonResponse({'data' : data, 'paging' : paging}, status = 200)
    
    
class BestView(View) : 
    def get(self, request) :
        viewPage     = request.GET.get('viewPage', None)
        sort         = request.GET.get('sort_type', None)
        
        product_list = Product.objects.order_by('-sales_index')[:99]
        
        paginator = sorting(product_list, sort)
        
        try:
            contacts = paginator.page(viewPage)
            
        except PageNotAnInteger:
            contacts = paginator.page(1)   
        
        except EmptyPage:
            return HttpResponse(status = 400) 
        
        products = product_info(contacts)
        
        data = {
            'category_name'         : '베스트',
            'products'              : products
        }
        
        paging = {
            'total'                 : product_list.count(),
            'total_page_no'         : paginator.num_pages
        }
        return JsonResponse({'data' : data, 'paging' : paging}, status = 200)
    

class SaleView(View) : 
    def get(self, request) :
        viewPage     = request.GET.get('viewPage', None)
        sort         = request.GET.get('sort_type', None)
        
        product_list = Product.objects.exclude(discount_percent = 0)
        
        paginator = sorting(product_list, sort)
        
        try:
            contacts = paginator.page(viewPage)
            
        except PageNotAnInteger:
            contacts = paginator.page(1)   
        
        except EmptyPage:
            return HttpResponse(status = 400) 
        
        products = product_info(contacts)
        
        data = {
            'category_name'         : '알뜰쇼핑',
            'products'              : products
        }
        
        paging = {
            'total'                 : product_list.count(),
            'total_page_no'         : paginator.num_pages
        }
        return JsonResponse({'data' : data, 'paging' : paging}, status = 200)
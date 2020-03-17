import json

from .models            import MainCategory, SubCategory

from django.views       import View
from django.http        import HttpResponse, JsonResponse 

class CategoryView(View):
    def get(self, request):
        category_list = [
            {       
                'main_category'         : main.name,
                'icon_black_url'        : main.icon_black_url,
                'icon_active_url'       : main.icon_active_url,
                'subcategory'           : [{
                    'name'          : sub.name, 
                    'thumbnail_url' : sub.thumbnail_url
                } for sub in SubCategory.objects.filter(maincategory = main.id).all()] 
            }
            for main in MainCategory.objects.all()
        ]

        return JsonResponse({"data" : list(category_list)}, status = 200)


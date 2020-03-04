import json

from .models import MainCategory, SubCategory

from django.views import View
from django.http import HttpResponse, JsonResponse 
from django.db.models import Prefetch

class CategoryView(View):
    def get(self, request):
        category_list = []
        for main in range(MainCategory.objects.count()) :
            subcate = []
            for sub in list(SubCategory.objects.filter(maincategory_id = main + 1)):
                subcate.append(
                    {
                        'name'          : sub.name, 
                        'thumbnail_url' : sub.thumbnail_url
                    }
                )
            category_list.append ({'main_category'        : MainCategory.objects.all()[main].name,
                                    'icon_black_url'      : MainCategory.objects.all()[main].icon_black_url,
                                    'icon_active_url'      : MainCategory.objects.all()[main].icon_active_url,
                                    'subcategory'         : subcate })

        return JsonResponse({"data" : list(category_list)}, status = 200)
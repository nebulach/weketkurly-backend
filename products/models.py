from django.db import models

class MainCategory(models.Model):
    name            = models.CharField(max_length = 50)
    icon_black_url  = models.CharField(max_length = 2000)
    icon_active_url = models.CharField(max_length = 2000)

    class Meta : 
        db_table = 'main_categories'


class SubCategory(models.Model):
    maincategory = models.ForeignKey('MainCategory', on_delete = models.CASCADE, related_name='subcategory')
    name            = models.CharField(max_length = 50)
    thumbnail_url   = models.CharField(max_length = 2000, blank = True, null = True)

    class Meta :
        db_table = 'sub_categories'

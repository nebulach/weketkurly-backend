from users.models   import User
from django.db      import models


class MainCategory(models.Model):
    name            = models.CharField(max_length = 50)
    icon_black_url  = models.URLField(max_length = 2000, null = True)
    icon_active_url = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = 'main_categories'


class SubCategory(models.Model):
    maincategory    = models.ForeignKey('MainCategory', on_delete = models.SET_NULL, blank = True, null = True)
    name            = models.CharField(max_length = 50)
    thumbnail_url   = models.URLField(max_length = 2000, blank = True, null = True)

    class Meta:
        db_table = 'sub_categories'


class Product(models.Model):
    sub_category            = models.ForeignKey('SubCategory', on_delete = models.SET_NULL, blank = True, null = True)
    name                    = models.CharField(max_length = 100)
    short_description       = models.CharField(max_length = 200, blank = True, null = True)
    unit_text               = models.CharField(max_length = 50, blank = True, null = True)
    weight                  = models.CharField(max_length = 50, blank = True, null = True)
    origin                  = models.CharField(max_length = 300, blank = True, null = True)
    expiration_date         = models.CharField(max_length = 500, blank = True, null = True)
    packing_type_text       = models.CharField(max_length = 300, blank = True, null = True)
    delivery_time_type_text = models.CharField(max_length = 300, blank = True, null = True)
    original_price          = models.IntegerField()
    discount_percent        = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    sales_index             = models.IntegerField(default = 0)
    contactant              = models.CharField(max_length = 500, blank = True, null = True)
    cart_image_url          = models.URLField(max_length = 2000, blank = True, null = True)
    detail_image_url        = models.URLField(max_length = 2000, blank = True, null = True)
    list_image_url          = models.URLField(max_length = 2000, blank = True, null = True)
    incoming_date           = models.DateTimeField()
    tag                     = models.ManyToManyField('Tag', through='ProductTag')

    class Meta:
        db_table = 'products'


class DetailInfomation(models.Model):
    product                = models.ForeignKey('Product', models.CASCADE)
    product_description    = models.TextField(null = True)
    product_image          = models.TextField(null = True)
    product_infomation     = models.TextField(null = True)

    class Meta:
        db_table = 'detail_infomations'
        
        
class Package(models.Model) :
    product = models.ForeignKey('Product', models.CASCADE)
    name    = models.CharField(max_length = 100)
    
    class Meta:
        db_table = 'packages'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'


class ProductTag(models.Model):
    product = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
    tag     = models.ForeignKey('Tag', on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = 'products_tags'

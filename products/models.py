from users.models   import User

from django.db      import models

class MainCategory(models.Model):
    name            = models.CharField(max_length=50)
    icon_black_url  = models.URLField(max_length=2000)
    icon_active_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'main_categories'


class SubCategory(models.Model):
    main_category   = models.ForeignKey('MainCategory', models.SET_NULL, blank=True, null=True)
    name            = models.CharField(max_length=50)
    thumbnail_url   = models.URLField(max_length=2000, blank=True, null=True)

    class Meta:
        db_table = 'sub_categories'

class SpecialCategory(models.Model):
    name    = models.CharField(max_length=50)
    product = models.ManyToManyField('Product', through='SpecialCategoryProduct')

    class Meta:
        db_table = 'special_categories'

class SpecialCategoryProduct(models.Model):
    special_category    = models.ForeignKey('SpecialCategory', on_delete=models.SET_NULL, null=True)
    product             = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'special_categories_products'

class Product(models.Model):
    sub_category        = models.ForeignKey('SubCategory', models.SET_NULL, blank=True, null=True)
    name                = models.CharField(max_length=50)
    unit_text           = models.CharField(max_length=10)
    weight              = models.CharField(max_length=10)
    origin              = models.CharField(max_length=50)
    contactant          = models.CharField(max_length=300)
    expiration_date     = models.CharField(max_length=100)
    packing_type_text   = models.CharField(max_length=50)
    original_price      = models.IntegerField()
    discount_percent    = models.IntegerField()
    original_image_url  = models.URLField(max_length=2000)
    main_image_url      = models.URLField(max_length=2000)
    list_image_url      = models.URLField(max_length=2000)
    short_description   = models.CharField(max_length=200)
    sticker_image_url   = models.URLField(max_length=2000)
    detail_image_url    = models.URLField(max_length=2000)
    stocks              = models.IntegerField()
    tag                 = models.ManyToManyField('Tag', through='ProductTag')

    class Meta:
        db_table = 'products'

class DetailInfomation(models.Model):
    product                = models.ForeignKey('Product', models.CASCADE)
    product_description    = models.TextField()
    product_image          = models.TextField()
    product_infomation     = models.TextField()

    class Meta:
        db_table = 'detail_infomations'

class Review(models.Model):
    product         = models.ForeignKey('Product', models.CASCADE)
    index_no        = models.IntegerField()
    review_title    = models.CharField(max_length=100)
    review_contents = models.TextField()
    user            = models.ForeignKey('users.User', models.CASCADE, related_name='review')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'

class ProductTag(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    tag     = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'products_tags'

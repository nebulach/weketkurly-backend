import csv
import os

import django

from products.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeketKurly_backend.settings")
django.setup()

csv_path = './products_data_crawl.csv'

with open(csv_path, newline='') as csv_file:
    data_reader = csv.DictReader(csv_file)

    for row in data_reader:
        # debug
        print(row)
        product_model = Product(
            sub_category        = SubCategory.objects.get(name=row['sub_category']),
            name                = row.get('product_name'),
            unit_text           = row.get('unit_text', ''),
            weight              = row.get('weight', ''),
            origin              = row.get('origin', ''),
            contactant          = row.get('contactant', ''),
            expiration_date     = row.get('expiration_date', ''),
            packing_type_text   = row.get('packing_type_text', ''),
            original_price      = row.get('original_price', ''),
            discount_percent    = row.get('discount_percent', ''),
            original_image_url  = row.get('original_image_url', ''),
            main_image_url      = row.get('main_image_url', ''),
            list_image_url      = row.get('list_image_url', ''),
            short_description   = row.get('short_description', ''),
            sticker_image_url   = row.get('sticker_image_url', ''),
            detail_image_url    = row.get('detail_image_url', ''),
            stocks              = row.get('stocks')
        )

        product_model.save()

        DetailInfomation.objects.create(
            product             = Product.objects.get(id=product_model.id),
            product_description = row.get('desc' ,''),
            product_image       = row.get('image', ''),
            product_infomation  = row.get('info', ''),
        )


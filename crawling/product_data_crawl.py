import requests
import json
import csv
import random
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeketKurly_backend.settings")
django.setup()
from products.models import *
from bs4 import BeautifulSoup

category_req    = requests.get(f'https://api.kurly.com/v1/categories/')
category_data   = category_req.json()

main_category   = category_data['data']['categories']

main_dict       = {}
product_dict    = {}

result_file     = "products_data_crawl.csv"

for main in main_category:
    main_dict[(main['no'], main['name'])] = []
    
    for sub_category in main['categories']:
        main_dict[(main['no'], main['name'])].append((sub_category['no'], sub_category['name']))

#print(main_dict)

for key, value in main_dict.items():
    start_page = 1
    max_page = 2
    
    for val in value:
        while start_page < max_page:
            sub_no = val[0]
            products_req    = requests.get(f'https://api.kurly.com/v1/categories/{sub_no}?page_limit=99&page_no=\
                                           {start_page}&delivery_type=0&sort_type=0&ver=1583341590230')
            products_data   = products_req.json()

            products_list   = products_data['data'].get('products', None)

            if products_list:
                for product in products_list:
                    product_dict[(val[1], product['no'])] = product['name']
            
            start_page += 1

#print(product_dict)
product_crawl_list = []

for key, val in product_dict.items():
    sub_category    = key[0]
    product_no      = key[1]
    #print("product_no: ", product_no)
    product_name    = val
    product_req     = requests.get(f'https://www.kurly.com/shop/goods/goods_view.php?&goodsno={product_no}')
    product_req2    = requests.get(f'https://api.kurly.com/v3/home/products/{product_no}?&ver=1583404862438')
    product_data    = product_req2.json()
    product_html    = product_req.text
    product_soup    = BeautifulSoup(product_html, 'lxml')

    product_desc    = product_soup.select('#goods-description')
    product_image   = product_soup.select('#goods-image')
    product_info    = product_soup.select('#goods-infomation')

    product_page_data   = product_data['data']
    print(product_page_data)
    unit_text           = product_page_data.get('unit_text', '')
    weight              = product_page_data.get('weight', '')
    origin              = product_page_data.get('origin', '')
    contactant          = product_page_data.get('contactant', '')
    expiration_date     = product_page_data.get('expiration_date', '')
    packing_type_text   = product_page_data.get('packing_type_text', '')
    original_price      = product_page_data.get('original_price', 0)
    discount_percent    = product_page_data.get('discount_percent', 0)
    original_image_url  = product_page_data.get('original_image_url', '')
    main_image_url      = product_page_data.get('main_image_url', '')
    list_image_url      = product_page_data.get('list_image_url', '')
    short_description   = product_page_data.get('short_description', '')
    sticker_image_url   = product_page_data.get('sticker_image_url', '')
    detail_image_url    = product_page_data.get('detail_image_url', '')
    stocks              = random.randrange(1, 1000)
    
    desc    = ''
    image   = ''
    info    = ''
    
    if product_desc:
        desc    = product_desc[0]
    if product_image:
        image   = product_image[0]
    if product_info:
        info    = product_info[0]

    product_tuples = (sub_category, product_name, unit_text, weight, origin, contactant, expiration_date, packing_type_text,\
                      original_price, discount_percent, original_image_url, main_image_url, list_image_url, short_description,\
                      sticker_image_url, detail_image_url, stocks, desc, image, info)
    
    product_crawl_list.append(product_tuples)

with open(result_file, 'w+', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(('sub_category', 'product_name', 'unit_text', 'weight', 'origin', 'contactant', 'expiration_date',\
                         'packing_type_text', 'original_price', 'discount_percent', 'original_image_url', 'main_image_url',\
                         'list_image_url', 'short_description', 'sticker_image_url', 'detail_image_url', 'stocks',\
                         'desc', 'image', 'info'))
    
    for rowdata in product_crawl_list:
        csv_writer.writerow((rowdata[0], rowdata[1], rowdata[2], rowdata[3], rowdata[4], rowdata[5], rowdata[6], rowdata[7],\
                             rowdata[8], rowdata[9], rowdata[10], rowdata[11], rowdata[12], rowdata[13], rowdata[14],\
                             rowdata[15], rowdata[16], rowdata[17], rowdata[18], rowdata[19]))









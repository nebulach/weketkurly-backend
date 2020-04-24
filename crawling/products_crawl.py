import csv
import os
import re

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeketKurly_backend.settings')
django.setup()

from products.models import *

# -*- coding: utf-8 -*-
import requests
import json
import datetime

from random          import randint
from bs4             import BeautifulSoup
import pandas        as pd

URL = 'https://api.kurly.com/v1/categories/909001?page_limit=99&page_no=1&delivery_type=0&sort_type=0&ver=1585658859570'
obj = requests.get(URL)
objson = obj.json()

mCols = []
df = pd.DataFrame(columns = mCols)

sub_category_ids            = []
names                       = []
short_descriptions          = []
unit_texts                  = []
weights                     = [] 
origins                     = []
expiration_dates            = []
packing_type_texts          = []
delivery_time_type_texts    = []
original_prices             = []
discount_percents           = []
sales_indexs                = []
contactants                 = []
detail_image_urls           = []
cart_image_urls             = []
list_image_urls             = []
incoming_dates              = []
goods_descriptions          = []
goods_images                = []
goods_infomations           = []

def re_palce(tag):
    pattern  = re.compile(r'\s+')
    sentence = re.sub(pattern, ' ', tag).strip()
    return sentence

def get_category() :
    category = requests.get('https://api.kurly.com/v2/categories?ver=1')
    cate_json = category.json()['data']['categories']

    for main in cate_json :
        for sub in main['categories'] :
            sub_num = sub['no']
            get_nextpage(sub_num, 1)
            print('-----')
        
def get_nextpage(sub_num, last_num) :
    url = f'https://api.kurly.com/v1/categories/{sub_num}?page_limit=99&page_no={last_num}&delivery_type=0&sort_type=0&ver=1585658859570'
    url = requests.get(url)
    objson = url.json()
    print('page : ', last_num)
    
    try :
        last_num = objson['paging']['next_page_no']
        get_nextpage(sub_num, last_num)
        
    except KeyError :
        print('끝', last_num)
        get_products(sub_num, last_num)
        
    
def get_products(sub_num, page) :
    page = page + 1
    for i in range(1, page) :
        url = f'https://api.kurly.com/v1/categories/{sub_num}?page_limit=99&page_no={i}&delivery_type=0&sort_type=0&ver=1585658859570'
        url = requests.get(url)
        objson = url.json()
        sub = objson['data']['category_name']
        products = objson['data']['products']
        print('1 page') 
        print(sub)
            
        for product in products :
            product_num = product['no']
            url = f'https://api.kurly.com/v3/home/products/{product_num}?&ver=1585655639453'
            det_url = requests.get(url).json()
            det_url = det_url['data']
            sub_category_id = SubCategory.objects.get(name = sub).id
            sub_category_ids.append(sub_category_id)
            
            name = det_url.get('name', '')
            names.append(name)
                        
            short_description = det_url.get('short_description', '')
            short_descriptions.append(short_description)
            
            unit_text = det_url.get('unit_text', '')
            unit_texts.append(unit_text)
            
            weight = det_url.get('weight', '')
            weights.append(weight)
            
            origin = det_url.get('origin', '')
            origins.append(origin)
            
            expiration_date = det_url.get('expiration_date', '')
            expiration_dates.append(expiration_date)
            
            packing_type_text = det_url.get('packing_type_text', '')
            packing_type_texts.append(packing_type_text)
            
            delivery_time_type_text = det_url.get('delivery_time_type_text', '')
            delivery_time_type_texts.append(delivery_time_type_text)
            
            original_price = det_url.get('original_price', '')
            original_prices.append(original_price)
            
            discount_percent = det_url.get('discount_percent', '')
            discount_percents.append(discount_percent)
            
            sales_index = det_url.get('review_count', '')
            sales_indexs.append(sales_index)
            
            contactant = det_url.get('contactant', '')
            contactants.append(contactant)
            
            detail_image_url = det_url.get('original_image_url', '')
            detail_image_urls.append(detail_image_url)
            
            cart_image_url = det_url.get('list_image_url', '')
            cart_image_urls.append(cart_image_url)
            
            list_image_url = det_url.get('detail_image_url', '')
            list_image_urls.append(list_image_url)
            
            incoming_date = datetime.date(randint(2005,2020), randint(1,12),randint(1,28))
            incoming_dates.append(incoming_date)
            
            
            kurly_url = 'https://www.kurly.com/shop/goods/goods_view.php?&goodsno=' + product['no']
            k_url = requests.get(kurly_url)
            site_content = BeautifulSoup(k_url.content, 'html.parser')
            
            goods_description = site_content.find('div', id = 'goods-description')
            goods_descriptions.append(goods_description)
            
            goods_image = site_content.find('div', id = 'goods-image')
            goods_images.append(goods_image)
            
            goods_infomation = site_content.find('div', id = 'goods-infomation')
            goods_infomations.append(goods_infomation)
        
            
def get_data():
    get_category()
    
    df['name']                      = names
    df['sub_category_id']           = sub_category_ids
    df['unit_text']                 = unit_texts
    df['short_description']         = short_descriptions
    df['weight']                    = weights
    df['origin']                    = origins
    df['expiration_date']           = expiration_dates
    df['packing_type_text']         = packing_type_texts
    df['delivery_time_type_text']   = delivery_time_type_texts
    df['original_price']            = original_prices
    df['discount_percent']          = discount_percents
    df['sales_index']               = sales_indexs
    df['contactant']                = contactants
    df['detail_image_url']          = detail_image_urls
    df['cart_image_url']            = cart_image_urls
    df['list_image_urls']           = list_image_urls
    df['incoming_date']             = incoming_dates
    df['goods_description']         = goods_descriptions
    df['goods_image']               = goods_images
    df['goods_infomation']          = goods_infomations
    df.to_csv("./products.csv", encoding = 'utf8')  
    print('Done.')

get_data()


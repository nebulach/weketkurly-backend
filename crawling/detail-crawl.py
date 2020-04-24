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

mCols = []
df = pd.DataFrame(columns = mCols)

product_ids                 = []
product_descriptions        = []
product_images              = []
product_informations        = []


def re_palce(tag):
    pattern  = re.compile(r'\s+')
    sentence = re.sub(pattern, ' ', tag).strip()
    return sentence

def get_category() :
    category = requests.get('https://api.kurly.com/v2/categories?ver=1')
    cate_json = category.json()['data']['categories']

    for sub in cate_json[14]['categories'] :
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
            
            name = det_url.get('name', '')
            print(name)
            
            try :
                product_id = Product.objects.filter(name = name).last().id
                product_ids.append(product_id)
            
            except IndexError:
                continue
            
            except AttributeError: 
                continue
            
            kurly_url = 'https://www.kurly.com/shop/goods/goods_view.php?&goodsno=' + product['no']
            k_url = requests.get(kurly_url)
            site_content = BeautifulSoup(k_url.content, 'html.parser')
            
            product_description = site_content.find('div', id = 'goods-description')
            product_descriptions.append(product_description)
            
            product_image = site_content.find('div', id = 'goods-image')
            product_images.append(product_image)
            
            product_information = site_content.find('div', id = 'goods-infomation')
            product_informations.append(product_information)
            
            
def get_data():
    get_category()
    
    df['product_id']                = product_ids
    df['product_description']       = product_descriptions
    df['product_image']             = product_images
    df['product_information']       = product_informations
    
    df.to_csv("./detail14.csv", encoding = 'utf8')  
    print('Done.')

get_data()


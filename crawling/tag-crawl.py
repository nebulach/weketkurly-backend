#아직 하나도 안건드림. 복붙만 함 
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

from bs4             import BeautifulSoup
import pandas        as pd

mCols = []
df = pd.DataFrame(columns = mCols)

product_ids     = []
tag_ids         = []


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

def get_nextpage(sub_num, last_num) :
    url = f'https://api.kurly.com/v1/categories/{sub_num}?page_limit=99&page_no={last_num}&delivery_type=0&sort_type=0&ver=1585658859570'
    url = requests.get(url)
    objson = url.json()
    
    try :
        last_num = objson['paging']['next_page_no']
        get_nextpage(sub_num, last_num)
        
    except KeyError :
        get_products(sub_num, last_num)
        
    
def get_products(sub_num, page) :
    page = page + 1
    for i in range(1, page) :
        url = f'https://api.kurly.com/v1/categories/{sub_num}?page_limit=99&page_no={i}&delivery_type=0&sort_type=0&ver=1585658859570'
        url = requests.get(url)
        objson = url.json()
        products = objson['data']['products']
            
        for product in products :
            tags = product['tags']['names']
            if tags:
                name = product['name']
                for tag in tags :
                    try :
                        product_id = Product.objects.filter(name = name).first().id
                        product_ids.append(product_id)
                        tag_id = Tag.objects.get(name = tag).id
                        tag_ids.append(tag_id)
                    
                    except IndexError:
                        continue
                    
                    except AttributeError: 
                        continue
                
            
            
def get_data():
    get_category()
    
    df['product_id']    = product_ids
    df['tag_id']        = tag_ids
    
    df.to_csv("./tag14.csv", encoding = 'utf8')  
    print('Done.')

get_data()
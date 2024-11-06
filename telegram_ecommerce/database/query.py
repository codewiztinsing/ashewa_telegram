
from sqlalchemy import select
from sqlalchemy.dialects.mysql import match
import requests
from telegram_ecommerce.database import models
from telegram_ecommerce.database.models import Session
from telegram_ecommerce.utils.utils import hash_password
import time
base_url = "https://api.ashewa.com"

def user_exist(user_id):
    response = requests.get(f"{base_url}/bot/check-user/{user_id}/")
   
    if response:
        response  = response.json()
        return response.get("exists")
    return False


def is_admin(user_id):
    return False


def get_password(user_id):

    return "123456"
    # with Session() as session:
    #     user = session.get(models.Customer, user_id)
    #     return user.password_hash

def check_password(user_id, password):
    return hash_password(password) == get_password(user_id)

def get_name_of_all_categories():
    all_categories = requests.get(f"{base_url}/bot/categories/")
    if all_categories != None:
        all_categories = all_categories.json()
        
    categories = []
    for item in all_categories:
        categories.append(item.get("name","Boss"))
    return categories
  

def get_category_id_from_name(name):
    return name
 


def get_all_available_by_category_id(name):
    products_from_api = requests.get(f"{base_url}/bot/products/?parent_category={name}")
    if products_from_api !=None:
        products_from_api=products_from_api.json()
        return products_from_api
      
    return []
  

def get_all_available_by_category_name(name):
    category_id = get_category_id_from_name(name)
    return get_all_available_by_category_id(name)

def get_ratings_of_a_product(product_id):

    return 5
  

def count_occurrence_of_specified_rating(product_id, rating):
    all_ratings = get_ratings_of_a_product(product_id)
    return 5
def search_products(string_to_search):
    data = requests.get(f"{base_url}/search/?keyword={string_to_search}")
    _data = []
    for d in data.json():
        _data.append({
            "id":d.get("id"),
            "name":d.get("name"),
            "price":d.get("selling_price",15),
            "description":d.get("name"),
            "quantity":10
        })
    return _data




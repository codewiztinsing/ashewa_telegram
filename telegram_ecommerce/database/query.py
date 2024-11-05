
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
    print("user data = ",response)
    if response:
        response  = response.json()
        return response.get("exists")
    return False
    # with Session() as session:
    #     return bool(session.get(models.Customer, user_id))

def is_admin(user_id):
    return False
    # with Session() as session:
    #     user = session.get(models.Customer, user_id)
    #     return user.is_admin if user else False

def get_password(user_id):

    return "123456"
    # with Session() as session:
    #     user = session.get(models.Customer, user_id)
    #     return user.password_hash

def check_password(user_id, password):
    return hash_password(password) == get_password(user_id)

def get_name_of_all_categories():
    all_categories = requests.get("https://api.ashewa.com/bot/categories/")
    if all_categories != None:
        all_categories = all_categories.json()
        
    categories = []
    for item in all_categories:
        categories.append(item.get("name","Boss"))
    return categories
  

def get_category_id_from_name(name):
    with Session() as session:
        stmt = select(models.Category.id).where(models.Category.name == name)
        return session.scalars(stmt).first()


def get_all_available_by_category_id(name):
    products_from_api = requests.get(f"https://api.ashewa.com/bot/products/?parent_category={name}")
    if products_from_api !=None:
        products_from_api=products_from_api.json()
        return products_from_api
      
    return []
    # with Session() as session:
    #     stmt = (
    #         select(models.Product)
    #         .where(models.Product.category_id == name)
    #         .where(models.Product.quantity_in_stock > 0)
    #     )
    #     return session.scalars(stmt).all()

def get_all_available_by_category_name(name):
    category_id = get_category_id_from_name(name)
    return get_all_available_by_category_id(name)

def get_ratings_of_a_product(product_id):
    return None
    # with Session() as session:
    #     stmt = (
    #         select(models.Order.rating)
    #         .where(models.Order.product_id == product_id)
    #         .where(models.Order.rating != None)
    #     )
    #     return session.scalars(stmt).all()

def count_occurrence_of_specified_rating(product_id, rating):
    all_ratings = get_ratings_of_a_product(product_id)
    return all_ratings.count(rating)

def search_products(string_to_search):
    data = requests.get(f"https://api.ashewa.com/search/?keyword={string_to_search}")
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

    
    # with Session() as session:
    #     stmt = select(models.Product).where(
    #         match(models.Product.name, models.Product.description, against=string_to_search)
    #     )
    #     return session.scalars(stmt).all()


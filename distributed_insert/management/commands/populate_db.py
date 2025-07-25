import threading
from django.core.management.base import BaseCommand
from distributed_insert.models import User, Product, Order
from django.db import transaction

USERS = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
    {'id': 4, 'name': 'David', 'email': 'david@example.com'},
    {'id': 5, 'name': 'Eve', 'email': 'eve@example.com'},
    {'id': 6, 'name': 'Frank', 'email': 'frank@example.com'},
    {'id': 7, 'name': 'Grace', 'email': 'grace@example.com'},
    {'id': 8, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 9, 'name': 'Henry', 'email': 'henry@example.com'},
    {'id': 10, 'name': '', 'email': 'jane@example.com'},
]

PRODUCTS = [
    {'id': 1, 'name': 'Laptop', 'price': 1000.00},
    {'id': 2, 'name': 'Smartphone', 'price': 700.00},
    {'id': 3, 'name': 'Headphones', 'price': 150.00},
    {'id': 4, 'name': 'Monitor', 'price': 300.00},
    {'id': 5, 'name': 'Keyboard', 'price': 50.00},
    {'id': 6, 'name': 'Mouse', 'price': 30.00},
    {'id': 7, 'name': 'Laptop', 'price': 1000.00},
    {'id': 8, 'name': 'Smartwatch', 'price': 250.00},
    {'id': 9, 'name': 'Gaming Chair', 'price': 500.00},
    {'id': 10, 'name': 'Earbuds', 'price': -50.00},
]

ORDERS = [
    {'id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2},
    {'id': 2, 'user_id': 2, 'product_id': 2, 'quantity': 1},
    {'id': 3, 'user_id': 3, 'product_id': 3, 'quantity': 5},
    {'id': 4, 'user_id': 4, 'product_id': 4, 'quantity': 1},
    {'id': 5, 'user_id': 5, 'product_id': 5, 'quantity': 3},
    {'id': 6, 'user_id': 6, 'product_id': 6, 'quantity': 4},
    {'id': 7, 'user_id': 7, 'product_id': 7, 'quantity': 2},
    {'id': 8, 'user_id': 8, 'product_id': 8, 'quantity': 0},
    {'id': 9, 'user_id': 9, 'product_id': 1, 'quantity': -1},
    {'id': 10, 'user_id': 10, 'product_id': 11, 'quantity': 2},
]

def validate_user(user):
    errors = []
    if not user['email']:
        errors.append("Email cannot be empty")
    if not user['name']:
        errors.append("Name cannot be empty")
    return errors

def validate_product(product):
    errors = []
    if product['price'] <= 0:
        errors.append("Price must be positive")
    if not product['name']:
        errors.append("Name cannot be empty")
    return errors

def validate_order(order):
    errors = []
    if order['quantity'] <= 0:
        errors.append("Quantity must be positive")
    if order['user_id'] < 1 or order['product_id'] < 1:
        errors.append("IDs must be positive")
    return errors

def insert_users():
    results = []
    for data in USERS:
        errors = validate_user(data)
        if errors:
            results.append({'data': data, 'success': False, 'errors': errors})
            continue
        try:
            with transaction.atomic(using='users'):
                User.objects.using('users').create(**data)
            results.append({'data': data, 'success': True, 'errors': None})
        except Exception as e:
            results.append({'data': data, 'success': False, 'errors': [str(e)]})
    print("User insert results:", results)
    return results

def insert_products():
    results = []
    for data in PRODUCTS:
        errors = validate_product(data)
        if errors:
            results.append({'data': data, 'success': False, 'errors': errors})
            continue
        try:
            with transaction.atomic(using='products'):
                Product.objects.using('products').create(**data)
            results.append({'data': data, 'success': True, 'errors': None})
        except Exception as e:
            results.append({'data': data, 'success': False, 'errors': [str(e)]})
    print("Product insert results:", results)
    return results

def insert_orders():
    results = []
    for data in ORDERS:
        errors = validate_order(data)
        if errors:
            results.append({'data': data, 'success': False, 'errors': errors})
            continue
        try:
            with transaction.atomic(using='orders'):
                Order.objects.using('orders').create(**data)
            results.append({'data': data, 'success': True, 'errors': None})
        except Exception as e:
            results.append({'data': data, 'success': False, 'errors': [str(e)]})
    print("Order insert results:", results)
    return results

class Command(BaseCommand):
    help = 'Populate databases concurrently'

    def handle(self, *args, **options):
        threads = []
        for func in [insert_users, insert_products, insert_orders]:
            t = threading.Thread(target=func)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

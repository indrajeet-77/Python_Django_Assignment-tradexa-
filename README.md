# Django Distributed System - Concurrent Database Operations

A Django-based distributed system simulation that manages multiple SQLite databases with concurrent thread-based insertions.

## 🎯 Project Overview

This project demonstrates a distributed system architecture where different data types (Users, Orders, Products) are stored in separate SQLite databases. The system performs simultaneous insert operations using multiple threads while maintaining data consistency and validation.

## 🏗️ Architecture

### Multi-Database Setup
- **users.db** - Stores User records
- **products.db** - Stores Product records  
- **orders.db** - Stores Order records
- **default.db** - Django's default database for admin and auth

### Models Structure

**User Model (users.db)**
- `id` - Primary Key (Integer)
- `name` - CharField (max_length=100)
- `email` - EmailField

**Product Model (products.db)**
- `id` - Primary Key (Integer)
- `name` - CharField (max_length=100)
- `price` - FloatField

**Order Model (orders.db)**
- `id` - Primary Key (Integer)
- `user_id` - IntegerField
- `product_id` - IntegerField
- `quantity` - IntegerField

## 🚀 Features

- ✅ **Multi-Database Architecture** - Separate SQLite databases for each model
- ✅ **Concurrent Processing** - Threading-based simultaneous insertions
- ✅ **Application-Level Validation** - All validations handled in Python
- ✅ **Custom Database Router** - Routes models to appropriate databases
- ✅ **Transaction Management** - Atomic transactions for data consistency
- ✅ **Error Handling** - Comprehensive validation and error reporting
- ✅ **Single Command Execution** - One command runs all operations

## 📋 Prerequisites

- Python 3.8+
- Django 4.x
- SQLite3 (comes with Python)

## 🛠️ Installation & Setup

1. **Clone/Extract the project**
   ```bash
   cd ds_project
   ```

2. **Install Dependencies**
   ```bash
   pip install django
   ```

3. **Run Migrations for All Databases**
   ```bash
   python manage.py makemigrations distributed_insert
   python manage.py migrate --database=users
   python manage.py migrate --database=products  
   python manage.py migrate --database=orders
   ```

4. **Execute the Concurrent Insertion**
   ```bash
   python manage.py populate_db
   ```

## 📊 Sample Data

The system processes 30 total records concurrently:

### Users (10 records)
```
1. Alice (alice@example.com)
2. Bob (bob@example.com)
3. Charlie (charlie@example.com)
...
10. [Empty name] - jane@example.com ❌ Validation Error
```

### Products (10 records)
```
1. Laptop ($1000.00)
2. Smartphone ($700.00)
3. Headphones ($150.00)
...
10. Earbuds ($-50.00) ❌ Validation Error
```

### Orders (10 records)
```
1. User:1, Product:1, Qty:2
2. User:2, Product:2, Qty:1
...
8. User:8, Product:8, Qty:0 ❌ Validation Error
9. User:9, Product:1, Qty:-1 ❌ Validation Error
10. User:10, Product:11, Qty:2 ❌ Invalid References
```

## 🔍 Validation Rules

### User Validation
- Email cannot be empty
- Name cannot be empty

### Product Validation  
- Price must be positive (> 0)
- Name cannot be empty

### Order Validation
- Quantity must be positive (> 0)
- User ID and Product ID must be positive integers

## 🧵 Threading Implementation

The system uses Python's `threading` module to perform concurrent insertions:

```python
threads = []
for func in [insert_users, insert_products, insert_orders]:
    t = threading.Thread(target=func)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

Each function processes its respective data independently, ensuring true concurrent execution.

## 📁 Project Structure

```
ds_project/
├── distributed_insert/
│   ├── management/
│   │   └── commands/
│   │       └── populate_db.py    # Main execution command
│   ├── migrations/               # Database migrations
│   ├── models.py                # Django models
│   ├── apps.py
│   └── views.py
├── ds_project/
│   ├── settings.py              # Multi-database configuration
│   ├── router.py                # Database routing logic
│   └── urls.py
├── users.db                     # Users SQLite database
├── products.db                  # Products SQLite database
├── orders.db                    # Orders SQLite database
├── default.db                   # Default Django database
└── manage.py
```

## 🎯 Expected Output

When running `python manage.py populate_db`, you'll see:

```
Order insert results: [
  {'data': {'id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2}, 'success': True, 'errors': None},
  {'data': {'id': 2, 'user_id': 2, 'product_id': 2, 'quantity': 1}, 'success': True, 'errors': None},
  ...
  {'data': {'id': 8, 'user_id': 8, 'product_id': 8, 'quantity': 0}, 'success': False, 'errors': ['Quantity must be positive']},
  ...
]

User insert results: [
  {'data': {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}, 'success': True, 'errors': None},
  ...
  {'data': {'id': 10, 'name': '', 'email': 'jane@example.com'}, 'success': False, 'errors': ['Name cannot be empty']},
  ...
]

Product insert results: [
  {'data': {'id': 1, 'name': 'Laptop', 'price': 1000.0}, 'success': True, 'errors': None},
  ...
  {'data': {'id': 10, 'name': 'Earbuds', 'price': -50.0}, 'success': False, 'errors': ['Price must be positive']},
  ...
]
```

## 📸 Screenshots

### Django Models Implementation
![Django Models](screenshots/02-models-code.png)
*Django models for User, Product, and Order with separate database configurations*

### Sample Data Arrays
![Sample Data](screenshots/04-sample-data.png)
*Test data arrays with validation test cases*

### Validation Functions
![Validation Logic](screenshots/04-validation-logic.png)
*Application-level validation functions for each model*

### Management Command Implementation
![Populate Command Part 1](screenshots/03-populate-command-part1.png)
![Populate Command Part 2](screenshots/03-populate-command-part2.png)
*Threading-based concurrent insertion logic and command structure*

### Database Router Configuration
![Database Router](screenshots/05-database-router.png)
*Custom router directing models to respective databases*

### Database Migrations Process
![Make Migrations](screenshots/06-makemigrations.png)
*Creating migrations for the distributed_insert app*

![Users Migration](screenshots/07-migration-users.png)
*Applying migrations to users.db*

![Products Migration](screenshots/08-migration-products.png)
*Applying migrations to products.db*

![Orders Migration](screenshots/09-migration-orders.png)
*Applying migrations to orders.db*

### Final Execution Results
![Final Output](screenshots/10-final-output.png)
*Concurrent insertion results showing successful operations and validation errors*

## 🔧 Configuration Details

### Database Settings (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'default.db',
    },
    'users': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'users.db',
    },
    'products': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'products.db',
    },
    'orders': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'orders.db',
    }
}
```

### Database Router (router.py)
Routes each model to its designated database based on the model name and app label.

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**
   - Ensure all databases are migrated: `python manage.py migrate --database=<db_name>`

2. **Import Errors**
   - Verify Django is installed: `pip install django`

3. **Database Lock Issues**
   - SQLite handles concurrent writes automatically, but if issues persist, check file permissions

4. **Threading Issues**
   - The system uses `transaction.atomic()` to ensure data consistency across threads

## 📈 Performance Notes

- **Concurrent Execution**: All three insertion functions run simultaneously
- **Database Isolation**: Each database operates independently
- **Transaction Safety**: Atomic transactions ensure data consistency
- **Validation Efficiency**: Application-level validation prevents invalid data insertion

## 🤝 Contributing

This is an assignment project demonstrating distributed system concepts with Django. The implementation focuses on:
- Multi-database architecture
- Concurrent processing
- Data validation
- Error handling
- Transaction management

## 📄 License

This project is created for educational purposes as part of a Python Django Developer assignment.

---

**Assignment Completed By**: [Your Name]  
**Date**: [Current Date]  
**Django Version**: 4.x  
**Python Version**: 3.8+

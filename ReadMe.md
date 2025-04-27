# Pokémon Store

## Overview
**Pokémon Store** is a Django-based web application that allows users to browse, search, and purchase Pokémon in a virtual store. It integrates real Pokémon data from [PokéAPI](https://pokeapi.co/) and supplements it with virtual Pokémon generated using the Faker library. Key features include:

- Browsing Pokémon with pagination and categorization (Real / Virtual)
- Advanced search by name, type, price range, and geographical location (latitude and longitude)
- Shopping cart system for adding, removing, and checking out Pokémon
- User authentication with registration, login, and logout
- Order history and detailed order views
- Admin dashboard for superusers to monitor orders and revenue

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Setup Steps

#### 1. Clone the repository
```bash
git clone <your-repo-url>
cd pokemon_store
```

#### 2. Install dependencies
Ensure you have a `requirements.txt` file with the following dependencies:

```text
Django==4.2
dj-database-url==2.2.0
requests==2.31.0
gunicorn==22.0.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
faker==25.8.0
```
Install them by running:

```bash
pip install -r requirements.txt
```

#### 3. Set up the database
Apply the migrations to create the necessary database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4. Import Pokémon data
Populate the database with Pokémon data using the custom management command:

```bash
python manage.py import_pokemon
```
This imports approximately 2,000 Pokémon records (898 real Pokémon from PokéAPI and 1,102 virtual Pokémon generated using Faker).

#### 5. Start the development server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 6. Access the application
Open your browser and visit:

```
http://localhost:8000/
```

---

## Data Overview

- **Real Pokémon**: 898 records (imported from PokéAPI)
- **Virtual Pokémon**: 1,102 records (generated with Faker)

> **Note**: The project requires 2,000–7,000 records. Due to time constraints and cloud database limitations, the current dataset meets the minimum requirement.

---

## Superuser Access

Default superuser credentials:

- **Username**: `qihangwan`
- **Password**: `qihangwan123`

To log in:

- Go to `/login/` and enter the superuser credentials
- Access the admin dashboard at `/dashboard/` to view order statistics

---

## Features

- **Pokémon Browsing**
  - Paginated list (100 Pokémon per page)
  - Categorized as Real (from PokéAPI) or Virtual (generated)

- **Advanced Search**
  - Search by name, type, price range, and location range (latitude and longitude)
  - Example: Find Pokémon within a specific geographical area

- **Shopping Cart**
  - Add Pokémon to cart with an "Add to Cart" button
  - View and manage cart contents
  - Proceed to checkout and place orders

- **User Authentication**
  - Register at `/register/`
  - Login at `/login/`
  - Logout at `/logout/`
  - View order history at `/orders/`

- **Admin Dashboard**
  - Accessible for superusers at `/dashboard/`
  - Displays total orders, total revenue, and Pokémon type distribution

---

## Testing

Unit tests are implemented to ensure the functionality of the application.

Run tests with:

```bash
python manage.py test
```

Tests cover:

- **Models** (e.g., Pokémon, Cart, Order)
- **Views** (e.g., Pokémon list, cart, checkout)
- **Search functionality** (name, type, price range, location range)
- **Error handling** (e.g., 404 pages)
- **Management commands** (e.g., `import_pokemon`)

---

## Deployment

The project is currently deployed on Codio:

> **URL**: https://dialoginclude-tommylady-8000.codio-box.uk:8000/

For production deployment (e.g., on Heroku):

- Switch to PostgreSQL (already supported via `psycopg2-binary`)
- Configure environment variables (e.g., `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`)
- Use Gunicorn as the WSGI server (already included)
- Serve static files using Whitenoise (already configured)

---

## License

This project is intended for educational and demonstration purposes only.  
For commercial use, please contact the developer.

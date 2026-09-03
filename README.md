# 🍲 RecipeShare

RecipeShare is a full-stack recipe sharing web application built with Django. Users can explore recipes, search and filter recipes by category, create and manage their own recipes, save recipes for later, and interact with recipes through reviews and ratings.

## 🚀 Features

### 👨‍🍳 Recipe Management
- View all recipes
- View detailed recipe information
- Search recipes
- Filter recipes by category
- Add new recipes
- Edit own recipes
- Delete own recipes
- Upload recipe images
- View personal recipes

### 🔐 Authentication
- User registration
- User login
- User logout
- Django authentication system
- Protected user-specific pages

### 🔖 Saved Recipes
- Save recipes for later
- View saved recipes
- Remove recipes from saved list

### ⭐ Reviews and Ratings
- Add reviews to recipes
- Rate recipes
- View recipe reviews

### 🏷️ Categories
- Organize recipes by category
- Browse recipes based on categories

### 👤 User Features
- My Recipes page
- Create personal recipes
- Manage personal recipes

### 👨‍💼 Admin Features
- Manage recipes
- Manage categories
- Manage users
- Manage reviews

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django ORM

### Database
- MySQL

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

### Other Technologies
- Django Authentication
- Pillow
- python-dotenv

---

## 📁 Project Structure

```text
RecipeShare/
│
├── recipeshare/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── recipes/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── accounts/
│   ├── home/
│   ├── recipes/
│   ├── reviews/
│   └── base.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │
│   └── js/
│       └── script.js
│
├── media/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```
## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SankarapuKavya/RecipeShare.git
```

### 2. Navigate to the Project Folder

```bash
cd RecipeShare
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the main project directory.

Add the following:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=recipeshare_db
DB_USER=root
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
```

⚠️ Never upload your actual `.env` file to GitHub.

---

## 🗄️ Database Setup

Create a MySQL database:

```sql
CREATE DATABASE recipeshare_db;
```

Then run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👨‍💼 Create an Admin User

To create a Django admin account:

```bash
python manage.py createsuperuser
```

Access the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

## ▶️ Run the Project

Start the Django development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

---

## 🔒 Security

Sensitive information such as the Django secret key and database credentials are stored in environment variables.

The actual `.env` file is excluded from GitHub using `.gitignore`.

An `.env.example` file is included to show the required environment variables.

---

## 🎯 Future Improvements

- User profile pages
- Advanced search and filtering
- Pagination
- Improved review system
- Responsive UI improvements
- REST API integration
- Recipe recommendations

---

## 👩‍💻 Author

**Kavya Sankarapu**

GitHub: https://github.com/SankarapuKavya

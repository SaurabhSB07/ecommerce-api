# 🛒 E-Commerce REST API (Django REST Framework + PostgreSQL)

This project is a **backend-only E-Commerce API** built using **Django REST Framework (DRF)** and **PostgreSQL**.  
It implements core features like authentication, product management, cart, orders, and reviews with secure JWT authentication.

---

## 🚀 Features

### 🔑 Authentication & Authorization
- User Registration & Login  
- JWT Authentication (Access + Refresh Tokens)  
- Password Reset via Email (SMTP backend)  

### 📦 E-Commerce Modules
- Products (CRUD + Image Uploads)  
- Cart & Orders  
- Product Reviews & Ratings  

### ⚙️ Advanced API Features
- Pagination (Page, LimitOffset, Cursor)  
- Filtering & Search  
- Permissions (IsAdmin, IsAuthenticated, ReadOnly, etc.)  
- Throttling for rate-limiting  

### 🗄️ Database
- PostgreSQL integration for scalability and performance  

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Auth:** JWT (SimpleJWT)  
- **Others:** SMTP Email Backend, DRF Pagination, Filtering, Throttling  

---

## 📂 Project Structure

ecommerce-api/

│── ecommerce/ # Main project settings & URLs 

│── accounts/ # User authentication & profile APIs

│── products/ # Product, Review APIs

│── orders/ # Cart & Order management

│── requirements.txt # Dependencies

│── manage.py



---

## 🔑 API Endpoints (Examples)

### Authentication
- `POST /api/auth/register/` → Register new user
- `POST /api/auth/login/` → Login & get JWT tokens
- `POST /api/auth/token/refresh/` → Refresh JWT token
- `POST /api/auth/password-reset/` → Reset password via email

### Products
- `GET /api/products/` → List all products
- `POST /api/products/` → Add product (Admin only)
- `GET /api/products/{id}/` → Get product details

### Cart & Orders
- `POST /api/cart/` → Add to cart
- `POST /api/orders/` → Place order
- `GET /api/orders/` → View user orders

---

## ▶️ Setup Instructions

### 1.Clone the repository:

   git clone https://github.com/your-username/ecommerce-api.git
   
   cd ecommerce-api
   
### 2.Create & activate virtual environment:  

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
 
### 3.Install dependencies:

pip install -r requirements.txt

### 4.Apply migrations:

python manage.py migrate

### 5.Create superuser:

python manage.py createsuperuser

### 6.Run server:

python manage.py runserver

## 📌 Future Improvements

Payment Gateway Integration

Wishlist & Address Management

Admin Dashboard for better analytics


## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

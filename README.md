# 🛒 Multi-Vendor E-Commerce Platform

A **feature-rich Multi-Vendor E-Commerce web application** built with **Django & Python**. This platform allows multiple vendors to sell their products, includes real-time messaging, order management, and secure payment integration.

## 🌟 Features
✅ **Multi-Vendor System** – Vendors can register, manage products & sales  
✅ **Real-Time Messaging** – Secure chat between buyers and sellers  
✅ **Product Management** – Add, edit, delete, and track inventory  
✅ **Order & Payment System** – Secure checkout with payment gateway integration  
✅ **User Authentication** – Buyers & vendors with separate dashboards  
✅ **Admin Panel** – Full control over vendors, products & transactions  
✅ **Reviews & Ratings** – Buyers can review & rate products  
✅ **Wishlist & Cart** – Save favorite products and add to cart  
✅ **Search & Filters** – Advanced product search with filters  

## 🛠️ Tech Stack
- **Backend:** Django, Django Rest Framework (DRF)  
- **Frontend:** HTML, CSS, JavaScript (Bootstrap/React)  
- **Database:** PostgreSQL / SQLite  
- **Messaging:** Django Channels (WebSockets for real-time chat)  
- **Deployment:** Docker, Gunicorn, Nginx  

## 📦 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment & activate it**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser for admin access**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

7. **Access the app**  
   - **Frontend:** `http://127.0.0.1:8000/`  
   - **Admin Panel:** `http://127.0.0.1:8000/admin/`  

## 🚀 Deployment Guide
- Set up a production server with **Gunicorn & Nginx**  
- Use **PostgreSQL** as the database  
- Deploy using **Docker** (optional)  

## 📜 License
This project is open-source and available under the **MIT License**.

---

📌 **GitHub Repository:** [https://github.com/costumebase/costumebase]  
📌 **Developer:** Rafi | MarsWebTech 🚀

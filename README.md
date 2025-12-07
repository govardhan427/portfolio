# Govardhan's Developer Portfolio "Masterpiece"

Welcome to **Govardhan's Developer Portfolio**! This is a **full-stack, production-grade application**, built with a **Django Rest Framework backend** and a **React frontend**. It goes beyond a simple static site by including a custom-built analytics engine, dynamic Open Graph image generation, and a fully manageable content dashboard.

---

## 📸 Project Preview
![Project Screenshot](https://res.cloudinary.com/dqw1t0dul/image/upload/v1765121885/Screenshot_2025-12-07_210620_xdlvfg.png)

---

## ✨ Features

### Frontend (React)
- **Interactive User Interface**: Built with React and Vite for lightning-fast performance, featuring a responsive design that works on all devices.
- **Dynamic Content Rendering**: Fetches Projects, Skills, Certificates, and Journey milestones directly from the backend API.
- **Admin Analytics Dashboard**: A protected dashboard visualizing real-time visitor stats, page views, and geolocation data using charts.
- **High-Impact Animations**: Smooth page transitions and interactive elements powered by Framer Motion.
- **Real-Time Contact Form**: Validated form submission that integrates seamlessly with the backend to send emails via Mailjet.

### Backend (Django Rest Framework)
- **Custom Analytics Engine**: A bespoke middleware-based tracking system that records unique visitors, session duration, online status, and geolocation (GeoIP) without relying on third-party scripts.
- **Dynamic Open Graph (OG) Images**: Automated generation of social media preview cards using **Python Pillow**. When a project is updated, a custom banner with the title and tagline is generated and saved automatically.
- **Secure Media Management**: Integration with **Cloudinary** to serve optimized images for projects and certificates via `URLField`s.
- **Robust Security**: Implemented CORS headers (credentials enabled), secure session cookies, and JWT authentication for the admin panel.
- **PostgreSQL Database**: Production-ready database schema with optimized migrations for analytics and content.

---

## 🛠️ Tech Stack

**Frontend:**
- Core: React, Vite
- Routing: React Router
- Styling: CSS Modules / Tailwind
- Animations: Framer Motion
- API Communication: Axios (with Interceptors)
- Charts: Recharts (for Dashboard)

**Backend:**
- Core: Django, Django Rest Framework (DRF)
- Analytics: Custom Middleware, GeoIP, User Sessions
- Image Processing: Pillow (PIL) for OG Generation
- Storage: Cloudinary
- Email: Mailjet REST API
- Database: PostgreSQL (Production) / SQLite3 (Local)

---

## 🚀 Local Setup and Installation

To run the project locally, **start both the backend and frontend servers** in separate terminals.

### Backend Setup (backend directory)
cd backend
### windows
- python -m venv venv
- .\venv\Scripts\activate
### install dependencies
- pip install -r requirements.txt
### Create a .env file in the backend directory:
#### add this
- SECRET_KEY='your-django-secret-key'
- DEBUG=True
- ALLOWED_HOSTS=127.0.0.1,localhost
- DATABASE_URL='sqlite:///db.sqlite3'
- CLOUDINARY_CLOUD_NAME='your-cloud-name'
- CLOUDINARY_API_KEY='your-api-key'
- CLOUDINARY_API_SECRET='your-api-secret'
- MAILJET_API_KEY='your-mailjet-key'
- MAILJET_API_SECRET='your-mailjet-secret'
- MAILJET_SENDER_EMAIL='your-verified-sender@email.com'
- MAILJET_RECEIVER_EMAIL='your-email@gmail.com'
### run migrations
- python manage.py migrate
### create superuser
- python manage.py createsuperuser
### start server
- python manage.py runserver
- The API will run at http://127.0.0.1:8000

## Frontend Setup (frontend directory)

- cd frontend
- npm install
- npm run dev
- The frontend will run at http://localhost:5173
. Open this URL in your browser to view the portfolio. To access the **Analytics Dashboard**, log in via the `/admin` route or the dedicated dashboard route using your superuser credentials.
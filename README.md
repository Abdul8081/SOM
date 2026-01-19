# Smart Order Management System (SOM)

A production-style backend system built using **Django** and **Django REST Framework** that handles **user authentication, order processing, payment workflows, notifications, async processing, caching infrastructure, and API documentation**.

---

## 🚀 Features Implemented

### 1. Authentication & Authorization

- JWT-based authentication using **djangorestframework-simplejwt**
- User registration and login APIs
- Protected endpoints using `IsAuthenticated`
- Role-aware user handling (normal users / staff)

---

### 2. Order Management

- Create orders with multiple items
- Automatic total amount calculation
- Fetch all orders for a user
- Fetch latest order
- Fetch order details securely (user-scoped)
- Order lifecycle management (`CREATED`, `PAID`)

---

### 3. Payment System (Mock Provider)

- Initiate payment for an order
- Confirm payment
- Idempotent payment initiation
- Automatic order status update on payment success
- Designed to be easily replaceable with real providers (Stripe/Razorpay)

---

### 4. Notifications (Async)

- Background notification processing using **Celery**
- Redis used as broker and result backend
- Notifications triggered on:
  - Order creation
  - Payment success
- Fully async & non-blocking
- Unit-tested Celery tasks

---

### 5. API Documentation (Swagger / OpenAPI)

- Integrated **drf-spectacular**
- Auto-generated Swagger UI
- Request & response schemas defined explicitly
- JWT Bearer authentication supported in Swagger UI
- Try-it-out enabled for all APIs

📍 Swagger URL:

---

### 6. Unit Testing

- API-level unit tests for:
  - Accounts
  - Orders
  - Payments
  - Notifications
- Isolated test database
- Mocked async tasks where required
- Command:

---

### 7. Containerized Setup

- Docker / Podman compatible
- Services included:
  - Django Web
  - PostgreSQL
  - Redis
  - Celery Worker
- Easy one-command startup

---

## 🧱 Tech Stack

| Layer     | Technology            |
| --------- | --------------------- |
| Backend   | Django 5.x            |
| API       | Django REST Framework |
| Auth      | JWT (SimpleJWT)       |
| DB        | PostgreSQL            |
| Async     | Celery                |
| Broker    | Redis                 |
| Docs      | drf-spectacular       |
| Testing   | Django Test Framework |
| Container | Docker / Podman       |

---

## 📁 Project Structure

SOM/
├── accounts/ # Authentication & user profile
├── orders/ # Order creation & management
├── payments/ # Payment workflows
├── notifications/ # Async notifications
├── SOM/ # Project settings
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## ⚙️ Environment Variables

Create a `.env` file:

POSTGRES_DB=smart_orders
POSTGRES_USER=smart_user
POSTGRES_PASSWORD=smart_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com

EMAIL_HOST_PASSWORD=your_app_password

STRIPE_SECRET_KEY=sk_test_xxxxx

---

## ▶️ Running the Project

1. podman-compose build
2. podman-compose up

## Post/api/v1/token

2. Copy `access` token
3. Click **Authorize** in Swagger
4. Enter:

---

## 📌 API Modules Covered

- `/api/v1/accounts/*`
- `/api/v1/orders/*`
- `/api/v1/payments/*`

All APIs are:

- Fully documented
- Auth-protected where required
- Tested

---

## 🧪 Current Status

| Feature             | Status                 |
| ------------------- | ---------------------- |
| Auth APIs           | ✅                     |
| Orders              | ✅                     |
| Payments (Mock)     | ✅                     |
| Async Notifications | ✅                     |
| Swagger Docs        | ✅                     |
| Unit Tests          | ✅                     |
| Email Integration   | Partially (SMTP ready) |
| Real Payments       | Planned                |
| Redis Caching       | Planned                |

---

## 🔮 Next Planned Enhancements

- Real payment gateway integration (Stripe)
- Redis-based query caching
- Email/SMS production-grade notifications
- Rate limiting & monitoring
- API versioning improvements

---

## 👨‍💻 Author

**Abdul Muid**  
Backend Developer | Django | Distributed Systems

---

## 📜 License

This project is for academic / evaluation / learning purposes.

#  Library Service API

A comprehensive Library Management System designed to automate book rentals, tracking, and payments. The system features real-time notifications via Telegram and automated fine calculations for overdue returns.

##  Key Features
* **User Management**: Secure JWT authentication and profile management.
* **Book Inventory**: Full CRUD for books with automated stock tracking.
* **Borrowing Logic**: Borrow books with inventory validation (prevents borrowing out-of-stock items).
* **Automated Payments**: Integrated with **Stripe API** for renting fees and overdue fines.
* **Telegram Notifications**: Instant alerts for new borrowings and returns.
* **Daily Overdue Check**: Automated **Celery Beat** tasks to notify administrators about overdue books every morning.
* **API Documentation**: Interactive documentation via Swagger.

## 🛠 Tech Stack
- **Python 3.12** / **Django** / **Django REST Framework**
- **PostgreSQL** (Database)
- **Redis** & **Celery** (Background tasks & scheduling)
- **Stripe API** (Payment processing)
- **Docker** & **Docker Compose** (Containerization)
- **Telegram Bot API**

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/nastyagst/Library-Service-Project.git]
cd library-service-api
```

### 2. Configure Environment Variables
##### Example .env content
POSTGRES_DB=library
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

STRIPE_SECRET_KEY=your_stripe_secret_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Create a Superuser
```bash
docker-compose exec app python manage.py createsuperuser
```

## API Documentation
**Once the server is running, you can access the documentation at:**
* Swagger: http://localhost:8000/api/doc/swagger/

## Testing & Code Quality
**The project is covered by a comprehensive test suite (Users, Books, Borrowings, Payments).**
```bash
docker-compose exec app python manage.py test
```

## Telegram Bot Features
**The bot notifies the administrator when:**

* **A new borrowing is created.**

* **A book is returned.**

* **Every morning, it sends a summary of all overdue borrowings (via Celery Beat).**

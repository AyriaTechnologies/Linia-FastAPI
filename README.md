# 🧬 Linia-FastAPI

**A modern, scalable FastAPI starter template by Ayria Technologies.**  
Built to accelerate your SaaS, API-first apps, and backend services with clarity and speed.

![FastAPI](https://img.shields.io/badge/FastAPI-async--ready-00c7a9?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square)
![License](https://img.shields.io/github/license/AyriaTechnologies/Linia-FastAPI?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue?style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-supported-ff5533?style=flat-square)

---

## 🚀 Features

Linia-FastAPI is a robust and feature-rich template designed to simplify and accelerate backend development. Here's what makes it special:

- ✅ **Modular Architecture** — Clean separation of routes, services, models, and schemas for maintainability and scalability.  
- 🔐 **JWT Authentication** — Secure login with OAuth2 password flow and refresh token support.  
- 💾 **PostgreSQL + SQLAlchemy** — Production-grade relational database setup with async support.  
- 🧰 **Pydantic** — Type-safe data validation and serialization for robust API contracts.  
- 🧪 **Testing Ready** — Pytest integration with Faker and isolated test database for seamless testing.  
- 🐳 **Dockerized** — Fully containerized with `docker-compose` for development and deployment.  
- 🔧 **Environment-Based Config** — Pydantic `BaseSettings` for managing environment variables.  
- 📄 **Auto API Docs** — Swagger UI and ReDoc automatically generated for your API.  
- 📈 **Scalable Design** — Perfect for MVPs, SaaS apps, and internal tools.  
- 🛠️ **Auto-Module Generator** — Automate the creation of new FastAPI modules with `auto-module.py`, including boilerplate for routes, schemas, models, and services.  
- ⚡ **Async-Ready** — Fully asynchronous design for high-performance APIs.  
- 🛡️ **Custom Exception Handling** — Centralized and extensible exception handling for better error management.  
- 📦 **Database Connection Pooling** — Optimized database connections with SQLAlchemy's async engine.  
- 🔄 **Alembic Migrations** — Version-controlled database schema migrations.  
- 🧹 **Code Quality** — Pre-configured with Flake8 and Ruff for linting and formatting.  
- 🔍 **Custom CRUD Utilities** — Reusable and generic CRUD operations for rapid development.  
- 🔄 **Token Management** — Comprehensive token generation and verification for access and refresh tokens.  
- 📜 **Customizable Templates** — Easily extendable templates for models, routes, and services.  

---

## 📁 Project Structure
```bash
Linia-FastAPI/
├── app/
│ ├── api/ # API routes (versioned)
│ ├── core/ # Config, security, utilities
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic
│ ├── db/ # DB setup and session
│ ├── User/ # Example module
│ │ ├── routes/ # User API routes
│ │ ├── schemas/ # Pydantic schemas
│ │ ├── models.py # SQLAlchemy models
│ │ ├── services.py # Business logic
│ │ ├── crud.py # CRUD operations
│ │ ├── apis.py # API integrations
│ │ ├── formatters.py # Data formatting helpers
│ │ ├── exceptions.py # Custom exceptions
│ │ ├── selectors.py # Query selectors
│ │ ├── annotations.py # Type hints/annotations
│ │ └── init.py # Module initializer
│ └── main.py # App entry point
├── tests/ # Unit and integration tests
├── auto-module.py # FastAPI module generator script
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/AyriaTechnologies/Linia-FastAPI.git
cd Linia-FastAPI
```

### 2. Create your .env file
```bash
cp .env.example .env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
fastapi dev
    or 
uvicorn app.main:app --reload
```
---

## 🛠️ Using auto-module.py
The auto-module.py script automates the creation of new FastAPI modules, saving you time and ensuring consistency. It generates the following structure for a new module:
```bash
app/
└── ModuleName/
    ├── routes/
    │   ├── __init__.py
    │   ├── base.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── create.py
    │   ├── edit.py
    │   ├── response.py
    ├── __init__.py
    ├── apis.py
    ├── models.py
    ├── services.py
    ├── selectors.py
    ├── exceptions.py
    └── formatters.py
```
### To create a new module, simply run:
```bash
python auto-module.py
```
Follow the prompts to specify the module name, and the script will handle the rest.

---
## 📦 Deployment Tips
- ✅ Use Nginx as a reverse proxy.

- ✅ Run with Gunicorn and uvicorn.workers.UvicornWorker in production.

- ✅ Store secrets securely using .env or a secret manager like AWS SSM, Vault, etc.

- ✅ Disable debug mode in production.

- ✅ Use observability tools like Sentry, Prometheus, or Grafana.
--- 
## 💡 About the Name
Linia (from "line") symbolizes clarity, structure, and elegant flow — the core values of Ayria’s software philosophy.
## 📄 License
MIT © Ayria Technologies
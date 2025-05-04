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
- ✅ **Modular Architecture** — clean separation of routes, services, models, and schemas  
- 🔐 **JWT Authentication** — secure login with OAuth2 password flow  
- 💾 **PostgreSQL + SQLAlchemy** — production-grade relational DB setup  
- 🧰 **Pydantic** — type-safe data validation and serialization  
- 🧪 **Testing Ready** — Pytest + Faker + isolated test database  
- 🐳 **Dockerized** — with `docker-compose` for dev & deployment  
- 🔧 **Environment-Based Config** — using Pydantic `BaseSettings`  
- 📄 **Auto API Docs** — Swagger UI and ReDoc out of the box  
- 📈 **Scalable Design** — perfect for MVPs, SaaS apps, and internal tools

---

## 📁 Project Structure
Linia-FastAPI/
├── app/
│   ├── api/                # API routes (versioned)
│   ├── core/               # Config, security, utilities
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── db/                 # DB setup and session
│   └── main.py             # App entry point
├── tests/                  # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md

---

## ⚙️ Getting Started

### 1. Clone the repo
```bash
### 2. Create your .env file
git clone https://github.com/AyriaTechnologies/Linia-FastAPI.git
cd Linia-FastAPI

cp .env.example .env

📦 Deployment Tips
✅ Use Nginx as a reverse proxy

✅ Run with Gunicorn + uvicorn.workers.UvicornWorker in production

✅ Store secrets using .env or a secret manager (e.g., AWS SSM, Vault)

💡 About the Name
Linia (from "line") symbolizes clarity, structure, and elegant flow — the core values of Ayria’s software philosophy.

📄 License
MIT © Ayria Technologies
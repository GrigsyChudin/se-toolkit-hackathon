# Link Manager API

**Problem:** Browser bookmarks are a mess, and links get lost in messengers.

**Solution:** A link manager with tags for quick grouping and easy search.

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy (async) + PostgreSQL
- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Database**: PostgreSQL 15
- **Package Manager**: uv (Python)
- **Reverse Proxy**: Nginx
- **Containerization**: Docker + Docker Compose

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings from .env
│   │   ├── database/            # Async database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── dependencies/        # Auth dependencies
│   │   └── errors/              # Custom error classes
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/                 # API client + services
│   │   ├── context/             # Auth + Theme contexts
│   │   ├── pages/               # Login, Register, Dashboard
│   │   └── types/               # TypeScript interfaces
│   ├── package.json
│   └── Dockerfile
├── nginx.conf                   # Nginx reverse proxy config
├── docker-compose.yml
└── .env.example
```

## Getting Started

### Local Development

```bash
docker-compose up --build -d
```

- Frontend: http://localhost:80
- Backend API: http://localhost
- Swagger Docs: http://localhost/docs

### Production Deployment

1. Create `.env` file:
```bash
cp .env.example .env
# Edit with your secrets
```

2. Deploy:
```bash
docker-compose up --build -d
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| POST | `/auth/refresh` | Refresh JWT token |
| GET | `/auth/me` | Get current user |

### Tags
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tags` | Get all user tags |
| POST | `/tags` | Create new tag |
| GET | `/tags/{id}` | Get tag by ID |
| PUT | `/tags/{id}` | Update tag |
| DELETE | `/tags/{id}` | Delete tag |

### Links
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/links` | Get all user links |
| POST | `/links` | Add new link |
| GET | `/links/{id}` | Get link by ID |
| PUT | `/links/{id}` | Update link |
| DELETE | `/links/{id}` | Delete link |
| GET | `/links/search/tags?tags=name` | Search by tags |
| GET | `/links/search/query?q=text` | Search by text |

## Features

- ✅ User registration and authentication (JWT)
- ✅ Link management (CRUD)
- ✅ Tag system with colors
- ✅ Many-to-many relationship: links ↔ tags
- ✅ Search by tags and text query
- ✅ User isolation (each user has their own data)
- ✅ Dark/Light theme toggle
- ✅ Swagger documentation at `/docs`
- ✅ Custom error codes for frontend handling
- ✅ Nginx reverse proxy

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| POSTGRES_USER | PostgreSQL username | postgres |
| POSTGRES_PASSWORD | PostgreSQL password | postgres |
| POSTGRES_DB | Database name | app |
| SECRET_KEY | JWT secret key | your-secret-key-change-in-production |

## Development

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

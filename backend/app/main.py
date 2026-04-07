from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import init_db
from app.routers import auth, links, tags

app = FastAPI(
    title="Link Manager API",
    description="""
## Link Manager with Tags

Problem: Browser bookmarks are a mess, and links get lost in messengers.

Solution: A link manager with tags for quick grouping and easy search.

### Features
- **User Authentication** - Register and login with JWT tokens
- **Link Management** - Add, update, delete links with descriptions
- **Tag System** - Create tags with colors for grouping links
- **Search** - Search links by tags or text query
- **User Isolation** - Each user has their own links

### Getting Started
1. Register a new user via `POST /auth/register`
2. Login via `POST /auth/login` to get a token
3. Create tags via `POST /tags`
4. Add links with tags via `POST /links`
5. Search links by tags or text

### Authentication
Click the **Authorize** button (top right) and enter your JWT token.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

# Define OpenAPI tags
app.openapi_tags = [
    {"name": "0. Health", "description": "Health check and API info"},
    {"name": "1. Authentication", "description": "User registration and login"},
    {"name": "2. Tags", "description": "Tag management for grouping links"},
    {"name": "3. Links", "description": "Link CRUD and search operations"},
]

# Add security scheme to OpenAPI
app.openapi_schema = None

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Ensure security scheme exists and is properly named
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    
    openapi_schema["components"]["securitySchemes"]["HTTPBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
    
    # Add security to protected endpoints
    protected_prefixes = ["/tags", "/links", "/auth/me", "/auth/refresh"]
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, operation in methods.items():
            if any(path.startswith(prefix) for prefix in protected_prefixes):
                operation["security"] = [{"HTTPBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tags.router)
app.include_router(links.router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get(
    "/",
    tags=["0. Health"],
    summary="API root",
    description="API root endpoint with basic information"
)
async def root():
    return {
        "name": "Link Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    tags=["0. Health"],
    summary="Health check",
    description="Check API health status"
)
async def health():
    return {
        "status": "ok",
        "service": "Link Manager API"
    }

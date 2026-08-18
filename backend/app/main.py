from .routers import contact
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import jobs
from .routers import admin
from .routers import products
from .routers import media
from fastapi.staticfiles import StaticFiles
from .routers import settings
from .routers import services
from .routers import projects
from .routers import applications
from .routers import partners
from .routers import gallery
from .routers import blog

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TerraLens API",
    version="1.0.0",
    description="Backend API for TerraLens Innovations",
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    contact.router,
    prefix="/contact",
    tags=["Contact"],
)

app.include_router(
    jobs.router,
    prefix="/jobs",
    tags=["Jobs"],
)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
)

app.include_router(
    products.router,
    prefix="/products",
    tags=["Products"],
)

app.include_router(
    media.router,
    prefix="/media",
    tags=["Media"],
)

app.include_router(
    settings.router,
    prefix="/settings",
    tags=["Settings"],
)

app.include_router(
    services.router,
    prefix="/services",
    tags=["Services"],
)

app.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"],
)

app.include_router(
    applications.router,
    prefix="/applications",
    tags=["Applications"],
)

app.include_router(
    partners.router,
    prefix="/partners",
    tags=["Partners"],
)

app.include_router(
    gallery.router,
    prefix="/gallery",
    tags=["Gallery"],
)

app.include_router(
    blog.router,
    prefix="/blogs",
    tags=["Blogs"],
)

@app.get("/")
def home():
    return {
        "message": "TerraLens Backend Running 🚀"
    }
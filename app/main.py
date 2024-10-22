from fastapi import FastAPI
from app.routers import cases, security, providers_router
from app.config.docs import docs_config


def create_app():
    app = FastAPI(**docs_config)
    app.include_router(security.router)
    app.include_router(cases.router)
    app.include_router(providers_router.router)

    return app

from fastapi import FastAPI
from app.routers import case_router, security_router
from app.config.docs import docs_config


def create_app():
    app = FastAPI(**docs_config)
    app.include_router(security_router)
    app.include_router(case_router)

    return app

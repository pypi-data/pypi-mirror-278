#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2024/6/11
# -------------------------------------------------------------------------------
from contextlib import asynccontextmanager

from fastapi import FastAPI, applications
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .config import settings
from .monkeypatch import get_redoc_html, get_swagger_ui_html


def dtp_application() -> FastAPI:
    """Create and initialize the FastAPI application."""
    app = create_app()
    return app


def create_app() -> FastAPI:
    """Create a FastAPI application with specified settings."""
    return FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=lifespan_manager,
    )


def register_routes(app: FastAPI) -> None:
    """Register application routes."""

    @app.get('/', include_in_schema=False)
    async def go_to_docs():
        """Redirect to documentation page."""
        return RedirectResponse(settings.DOCS_URL)

    @app.get("/health-check", include_in_schema=False)
    async def health_checks():
        """Perform a health check."""
        return 'ok'


@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    """Manage the application lifespan."""
    apply_docs_monkeypatch()
    mount_static_server(app)
    yield


def mount_static_server(app: FastAPI) -> None:
    """Mount the static file server."""
    app.mount(
        path=settings.DOCS_URL,
        app=StaticFiles(directory=settings.DOCS_ROOT),
        name='docs'
    )


def apply_docs_monkeypatch() -> None:
    """Apply monkeypatch for documentation resources."""
    setattr(applications, 'get_redoc_html', get_redoc_html)
    setattr(applications, 'get_swagger_ui_html', get_swagger_ui_html)

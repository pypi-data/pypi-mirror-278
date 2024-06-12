#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2024/6/11
# -------------------------------------------------------------------------------
from typing import Any
from fastapi.openapi.docs import get_redoc_html as _get_redoc_html
from fastapi.openapi.docs import get_swagger_ui_html as _get_swagger_ui_html

from dtprunner.config import settings


def get_static_url(path: str) -> str:
    """构造完整的静态资源URL."""
    return f'{settings.DOCS_URL}{path}'


def get_redoc_html(*args: Any, **kwargs: Any) -> Any:
    """从本地获取Redoc静态资源."""
    redoc_urls = {
        'redoc_favicon_url': get_static_url(settings.REDOC_ICON_STATIC_PATH),
        'redoc_js_url': get_static_url(settings.REDOC_JS_STATIC_PATH),
    }
    return _get_redoc_html(*args, **{**kwargs, **redoc_urls})


def get_swagger_ui_html(*args: Any, **kwargs: Any) -> Any:
    """从本地获取Swagger静态资源."""
    swagger_urls = {
        'swagger_favicon_url': get_static_url(settings.SWAGGER_ICON_STATIC_PATH),
        'swagger_js_url': get_static_url(settings.SWAGGER_JS_STATIC_PATH),
        'swagger_css_url': get_static_url(settings.SWAGGER_CSS_STATIC_PATH),
    }
    return _get_swagger_ui_html(*args, **{**kwargs, **swagger_urls})

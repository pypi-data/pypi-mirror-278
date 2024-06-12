#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2024/6/11
# -------------------------------------------------------------------------------
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ===========================================================================
    # 项目基本配置
    # ===========================================================================
    BASE_DIR: Path = Path(__file__).resolve().parent

    PROJECT_NAME: str = 'dtprunner'
    VERSION: str = '❄︎'

    SERVER_HOST: str = 'localhost'
    SERVER_PORT: int = 8000

    API_PREFIX: str = '/api'

    OPENAPI_URL: str = '/openapi.json'

    DOCS_URL: str = '/docs'
    DOCS_ROOT: Path = BASE_DIR / 'docs'

    # ===========================================================================
    # 静态资源配置
    # ===========================================================================
    SWAGGER_ICON_STATIC_PATH: str = '/swagger/favicon.png'
    SWAGGER_JS_STATIC_PATH: str = '/swagger/swagger-ui-bundle.js'
    SWAGGER_CSS_STATIC_PATH: str = '/swagger/swagger-ui.css'

    REDOC_ICON_STATIC_PATH: str = '/redoc/redoc-logo.png'
    REDOC_JS_STATIC_PATH: str = '/redoc/redoc.standalone.js'

    class Config:
        """Configuration for the Settings class."""
        env_file = '.env'
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get the cached settings instance."""
    return Settings()


settings = get_settings()


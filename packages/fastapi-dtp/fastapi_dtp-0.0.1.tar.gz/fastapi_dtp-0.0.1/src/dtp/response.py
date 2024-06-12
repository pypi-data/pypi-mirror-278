#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2024/6/11
# -------------------------------------------------------------------------------
from typing import Any, TypeVar, Generic, Optional, Dict

from pydantic import BaseModel


SCHEMA = TypeVar("SCHEMA")


class ResponseModel(BaseModel, Generic[SCHEMA]):
    code: int
    message: str
    data: Optional[SCHEMA]

    class Config:
        """ Configuration for pydantic model to allow generic types. """
        arbitrary_types_allowed = True


def response(code: int, message: str, data: Optional[SCHEMA]) -> Dict[str, Any]:
    """
    Generate a response dictionary using the ResponseModel.
    :param code: (int): Response code.
    :param message: (str): Response message.
    :param data: (Optional[SCHEMA]): Optional response data.
    :return: dict[str, Any]: Dictionary representation of the response model.
    """
    return ResponseModel(code=code, message=message, data=data).dict()


def resp_ok(data: Optional[SCHEMA] = None, code: int = 0, message: str = 'SUCCESS') -> Dict[str, Any]:
    """
    Generate a successful response.
    :param data: (Optional[SCHEMA], optional): Response data. Defaults to None.
    :param code: (int, optional): Response code. Defaults to 0.
    :param message: (str, optional): Response message. Defaults to 'SUCCESS'.
    :return: dict[str, Any]: Dictionary representation of the successful response.
    """
    return response(code=code, message=message, data=data)


def resp_err(message: str, code: int = 1, data: Optional[SCHEMA] = None) -> Dict[str, Any]:
    """
    Generate an error response.
    :param message: (str): Error message.
    :param code: (int, optional): Response code. Defaults to 1.
    :param data: (Optional[SCHEMA], optional): Optional response data. Defaults to None.
    :return: dict[str, Any]: Dictionary representation of the error response.
    """
    return response(code=code, message=message, data=data)

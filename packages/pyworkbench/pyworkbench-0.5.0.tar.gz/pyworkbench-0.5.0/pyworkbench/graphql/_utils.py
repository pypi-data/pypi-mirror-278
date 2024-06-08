"""Generate utilities for the GraphQL development"""
from typing import (
    Any, Union, Annotated,
    Optional, List,
    get_origin, get_args
)
from functools import cached_property
# Strawberry imports
import strawberry
from strawberry.fastapi import BaseContext
# Local imports
from pyworkbench.jwt_handler import JWTHandler

JWT = JWTHandler()


def is_optional(field: Any) -> bool:
    """Evaluate if a field is optional or not."""
    return get_origin(field) is Union and \
        type(None) in get_args(field)


def is_annotated(variable: Any) -> bool:
    """Evaluate if a function is annotated or not"""
    return get_origin(variable) == Annotated


def is_list(variable: Any) -> bool:
    """Evaluate if a field or model is a list"""
    if is_optional(variable):
        variable = get_args(variable)[0]
    return get_origin(variable) == list

def decapitalize(model: str) -> str:
    """Return a string in Camel format"""
    return model[0].lower() + model[1:]


def capitalize(model: str) -> str:
    """Return a string with the first letter capitalized"""
    return model[0].upper() + model[1:]


@strawberry.input
class FindBy:  # pylint: disable=R0903
    """FindBy method for inputs for the functions."""
    id: Optional[strawberry.ID] = strawberry.UNSET


@strawberry.input
class Filter:  # pylint: disable=R0903
    """Filter method for inputs"""
    id: Optional[strawberry.ID] = strawberry.UNSET
    ids: Optional[List[strawberry.ID]] = strawberry.UNSET


@strawberry.type
class Response:  # pylint: disable=R0903
    """Response for all the mutation types"""
    messages: Optional[str]
    successful: Optional[bool]


@strawberry.type
class UserLoginResponse:
    """Response comming from a User Login mutation"""
    token: str


@strawberry.type
class LoginResponse(Response):
    """Tell the success or failure of a login process"""
    result: Optional[UserLoginResponse]


class FastAPIContext(BaseContext):
    """Context for the executable session"""

    @cached_property
    def authenticated(self) -> bool:
        """Get the current user from the session cache"""
        if not self.request:
            return False

        token = self.request.headers.get("Authorization", None)
        if not token:
            return False
        # Evaluate if it has the Bearer
        if "Bearer" not in token:
            return False
        # Try to decode the token
        light_token = token.split("Bearer ")[-1]
        try:
            JWT.decode(light_token)
        except (Warning, ValueError):
            # If something bad happens, return None
            return False
        return True


class Error(Exception):
    """Object to return errors messages for different payloads."""

    def __init__(self,
                 message: str, status: str,
                 field: Optional[str] = None) -> None:
        # Define the arguments to use
        self.status = status
        self.message = message
        self.field = field

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.status!r}, detail={self.message!r})"

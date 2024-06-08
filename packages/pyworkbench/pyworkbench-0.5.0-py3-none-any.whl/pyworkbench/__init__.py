"""
A comprehensive toolkit for building and managing APIs in Python using FastAPI. 
This package includes modules for handling JWT authentication, database connections, 
automatic GraphQL API creation, advanced logging, and managing Uvicorn servers.

Modules:
- BaseApp: Base class for FastAPI applications.
- JWTHandler: Class for handling JWT tokens.
- DatabaseHandler: Class for managing database connections.
- GraphQL: Module for automatic creation of GraphQL APIs.
- Logger: Advanced logger for applications.
- Server: Class for managing Uvicorn servers with advanced functionalities.
"""
from .database_handler import DatabaseHandler
from .base_api import BaseAPI
from .server_handler import run_server, parse_args
from .logger import Logger

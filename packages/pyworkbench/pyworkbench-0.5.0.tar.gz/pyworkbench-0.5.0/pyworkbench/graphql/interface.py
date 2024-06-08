"""
Create a method to instance and serve the GraphQL API
into a FastAPI server
"""
from typing import Type, Any, Optional, Callable
# Strawberry imports
import strawberry
from strawberry.fastapi import GraphQLRouter
# FastAPI imports
from fastapi import FastAPI
from fastapi.responses import FileResponse
# Local imports
from pyworkbench.graphql.models_builder import models
from pyworkbench.graphql.connectors.template import DatabaseConnector
from pyworkbench.graphql.query_builder import QueryBuilder
from pyworkbench.graphql.mutation_builder import MutationBuilder
from pyworkbench.graphql._utils import FastAPIContext
from pyworkbench.jwt_handler import JWTHandler

JWT = JWTHandler()


def generate_graphql_schema(
    connector: Type[DatabaseConnector],
    connector_args: Optional[Any] = None,
    extra_query_methods: Optional[dict[str, Callable]] = None,
    extra_mutation_methods: Optional[dict[str, Callable]] = None
) -> strawberry.Schema:
    """Initialize a GraphQL Server"""
    # Init the QueryBuilder and MutationBuilder based on the connector that
    # the user share
    if not issubclass(connector, DatabaseConnector):
        raise ValueError("The connector must inheritance from `DatabaseConnector`.")
    # Init the connector
    if connector_args:
        if isinstance(connector, list):
            db_connect = connector(models, *connector_args)
        else:
            db_connect = connector(models, connector_args)
    else:
        db_connect = connector(models)
    # Now, init the QueryBuilder and MutationBuilder
    query_b = QueryBuilder(db_connect, extra_methods=extra_query_methods)
    mutation_b = MutationBuilder(
        db_connect, extra_methods=extra_mutation_methods)
    # First, create the GraphQL API with Strawberry and use it on the GraphQL app
    # from strawberry.asgi client. Just return that value.
    return strawberry.Schema(
        query=query_b.query,
        mutation=mutation_b.mutation
    )


def connect_to_fastapi(
    app_server: FastAPI,
    gql_schema: strawberry.Schema
) -> None:
    """Connect the generated schema to FastAPI"""
    graphql_router = GraphQLRouter(gql_schema, context_getter=get_context)
    app_server.include_router(graphql_router, prefix="/graphql")

async def custom_favicon():
    """Add custom favicon for a Router page"""
    return FileResponse("public/favicon.ico")

async def get_context() -> FastAPIContext:
    """Function to get the context elements. Only works for FastAPI"""
    return FastAPIContext()

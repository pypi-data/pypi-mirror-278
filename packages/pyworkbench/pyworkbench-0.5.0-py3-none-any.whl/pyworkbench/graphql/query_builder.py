"""
Python file that includes the Query object for the GraphQL
test API.
"""
from dataclasses import make_dataclass
from collections import deque
from typing import List, Union, Optional, Dict, Callable, Type, Annotated, get_origin, get_args
import strawberry
# Local imports
from pyworkbench.graphql._utils import (
    FindBy, Filter, FastAPIContext, Error,
    capitalize, is_optional, is_list
)
from pyworkbench.graphql.connectors.template import DatabaseConnector
from pyworkbench.graphql.models_builder import models, enums, find_by_models


# ---------------------------------------------------------------- #
#                          QUERY BUILDER                           #
# ---------------------------------------------------------------- #


class QueryBuilder:
    """Class that generates dynamically the Query object"""
    __slots__ = ['_query_obj', '_query_utils', '_models', '_enums']

    def __init__(
        self,
        connector: DatabaseConnector,
        extra_methods: Optional[dict[str, Callable]] = None,
    ) -> None:
        self._query_obj: Type = None  # Initialize the query object as Nothing

        # Init the models
        self._models = models
        self._enums = enums
        # Initialize the QueryUtils object
        self._query_utils = connector
        # ----------------------------------------------------------------
        # Call the build methods
        _methods = self.__build_methods()
        self.__build_query(_methods=_methods, extra_methods=extra_methods)

    @property
    def query(self) -> Type:
        """Method to return the query object as a property."""
        return self._query_obj

    def __find_by(self, model: str) -> Type[FindBy]:
        """Generate a unique findBy for each type.

        Args:
            - model (str): Model to generate its findBy

        Return:
            - The Strawberry input object
        """
        return find_by_models[model]

    def __filter(self, model: str) -> strawberry.input:  # type: ignore
        """Generate a unique orderBy for each type.

        Args:
        ---------------------------------------------------------------
            - model (str): Model to generate its findBy

        Return:
        ----------------------------------------------------------------
            - The Strawberry input object
        """
        _fields = []
        _model_hint = self._models[model] if model in self._models else self._enums[model]

        # Start to iterate over each hint of the model
        for attr, hint in _model_hint.__annotations__.items():
            if capitalize(attr) in self._enums:
                _type = self._enums[capitalize(attr)]
            elif is_optional(hint):
                if is_list(hint):
                    continue
                _type = [h for h in get_args(hint) if h and get_origin(h) is not Annotated][0]
            elif get_origin(hint) == Union:
                continue
            else:
                # If it's not a enum or a Union, then just return that hint
                _type = hint
            # Append it to the fields twice (one for the normal, other for the plural case)
            for _a, _t in [(attr, _type), (attr+'s', List[_type])]:
                _fields.append((_a, Optional[_t], strawberry.UNSET))

        # With this model, just return the input object
        return strawberry.input(make_dataclass(cls_name='Filters'+model,
                                               fields=_fields, bases=(Filter,)))

    def __order_by(self, model: str) -> strawberry.input:  # type: ignore
        """Generate a unique orderBy for each type.

        Args:
        ---------------------------------------------------------------
            - model (str): Model to generate its findBy

        Return:
        ----------------------------------------------------------------
            - The Strawberry input object
        """
        # Using the model, select from the enums the "Attributes" enum
        _attrs_enum = self._enums[model+'Attributes']
        # With this model, just return the input object
        return strawberry.input(make_dataclass(cls_name='OrderBy'+model,
                                               fields=(('asc', Optional[_attrs_enum], strawberry.UNSET),  # type: ignore
                                                       ('desc', Optional[_attrs_enum], strawberry.UNSET))))

    def __build_ind_func(self, model: str) -> Callable:
        """Method to build the functions to be used as individual
        methods.

        Args:
        ----------------------------------------------------------------
            - model (str): Model string to be used

        Returns:
        ----------------------------------------------------------------
            - Function to access the local data.
        """
        async def _n_function(
            info: strawberry.Info[FastAPIContext],
            id: Optional[strawberry.ID] = strawberry.UNSET,  # pylint: disable=W0622
            find_by: Optional[FindBy] = strawberry.UNSET,
        ) -> None:
            """Empty docstring to be updated later in this same code."""
            if info.context.authenticated is False:
                raise Error(message="Token or authorization not valid.",
                            status="500",
                            field="token"
                            )
            if not all(inp == strawberry.UNSET for inp in [id, find_by]):
                return self._query_utils.singular_search(  # type: ignore
                    model,
                    **find_by.__dict__
                )
            # If doesn't give any search value as ID or findBy option, then
            # return an error to the user.
            raise Error(message="You doesn't provide an ID or findBy argument to search" +
                        f" for the model {model}.",
                        status="500", field='query parameters')
        # ----------------------------------------------------------------
        # Now, change some parameters of this function
        _n_function.__name__ = self._query_utils.method_name(model)
        _n_function.__doc__ = f"Return a {model} model given an ID or a findBy method."
        _n_function.__annotations__[
            'return'] = Union[self._models[model], None]  # type: ignore
        # Get the corresponding FindBy class for this model
        _n_function.__annotations__[
            'find_by'] = Optional[self.__find_by(model)]
        # Finally, return the function
        return _n_function

    def __build_plural_func(self, model: str) -> Callable:
        """Method that would be used to generate dynamically the plural methods for
        to access to the information.

        Args:
        ----------------------------------------------------------------
            - model (str): Model string to be used

        Returns:
        ----------------------------------------------------------------
            - Function to access the local data.
        """
        async def _n_function(
            info: strawberry.Info[FastAPIContext],
            exclude: Optional[str] = strawberry.UNSET,
            filter: Optional[str] = strawberry.UNSET,  # pylint: disable=W0622
            limit: Optional[int] = strawberry.UNSET,
            order_by: Optional[str] = strawberry.UNSET,
                        ) -> None:
            """Empty docstring to be updated later in this same code."""
            if info.context.authenticated is False:
                raise Error(message="Token or authorization not valid.",
                            status="500",
                            field="token"
                            )

            # Perform the search with the QueryUtils object
            return self._query_utils.plural_search(obj_type=model, exclude=exclude, # type: ignore
                                                   filter=filter, limit=limit,
                                                   orderBy=order_by)
        # --------------------------------------------------------------
        # Now, change some parameters of this function
        _n_function.__name__ = self._query_utils.method_name(model, p=1)
        _n_function.__doc__ = f"Return the values for the model {model}" +\
            " in based of the given parameters."
        _n_function.__annotations__[
            'return'] = Union[List[self._models[model]], None]  # type: ignore
        _n_function.__annotations__['filter'] = Optional[self.__filter(model)]
        _n_function.__annotations__[
            'order_by'] = Optional[self.__order_by(model)]
        # Finally, return the function
        return _n_function

    def __build_methods(self) -> Dict[str, strawberry.field]:  # type: ignore
        """Method that would be used to generate
        dynamically the methods for the query"""
        _models = self._models.keys()
        _models = deque([m for m in _models if not m in self._enums])
        # Also, initialize the type generator for the query methods
        _query_methods = {}  # You'll define here the member functions of the obj

        # Do a while to generate the models
        while len(_models):
            # Select one model
            model = _models[0]
            # Append this new entry to the _query_methods and using the build_function method
            for model, func in [
                (self._query_utils.method_name(model),
                 self.__build_ind_func(model)),
                (self._query_utils.method_name(model, p=1),
                 self.__build_plural_func(model))
            ]:
                # Append the function with the model name as an method parameter
                _query_methods[model] = strawberry.field(
                    resolver=func, name=model)

            # Erase this element from the models list
            _models.popleft()
        # Also, add the enums to the _query_methods
        for enum_k, enum_v in self._enums.items():
            _query_methods[enum_k] = enum_v
        # Once the while has finished, return the intern methods
        return _query_methods

    def __build_query(self, **kwargs) -> None:
        """Method that would be used to generate the object of the Query method.

        Args:
            - kwargs (Dict[str, strawberry.field]): All the methods to append in the query object.
        """
        all_methods = {}
        for methods in kwargs.values():
            if methods:
                all_methods.update(methods)
        # Now, define the type of the obj
        query_obj = type('Query', (object, ), all_methods)
        self._query_obj = strawberry.type(query_obj)

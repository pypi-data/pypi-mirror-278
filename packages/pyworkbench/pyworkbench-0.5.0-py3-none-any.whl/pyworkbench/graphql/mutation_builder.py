"""
Python file that includes the Mutation object for the GraphQL API.
"""
from dataclasses import make_dataclass
from typing import (
    Type, Callable, Any,
    Dict, Union, Optional,
    get_origin, get_args
)
from collections import deque
import strawberry
# Local imports
from pyworkbench.graphql._utils import (
    FindBy, Response, FastAPIContext, Error,
    capitalize, is_annotated, is_list
)
from pyworkbench.graphql.connectors.template import DatabaseConnector
from pyworkbench.graphql.models_builder import (
    models, enums,
    find_by_models, response_by_model
)



class MutationBuilder:  # pylint: disable=R0903
    """Class that dynamically generates the MutationBuilder object"""

    def __init__(
        self,
        connector: DatabaseConnector,
        extra_methods: Optional[dict[str, Callable]] = None,
    ) -> None:
        self._mutation_obj: Type
        self._models = models
        self._enums = enums
        self._mutation_utils = connector
        _methods = self.__build_methods()
        self.__build_mutation(_methods=_methods, extra_methods=extra_methods)

    @property
    def mutation(self) -> Type:
        """Devuelve el objeto de mutación como propiedad."""
        return self._mutation_obj

    def __build_methods(self) -> Dict[str, Type]:
        """Method that dynamically generates the models"""
        _models = self._models.keys()
        _models = deque([m for m in _models if not m in self._enums])
        _mutation_methods = {}

        while len(_models):
            model = _models[0]
            for model, func in [
                (f"create{model}", self.__build_create_func(model)),
                (f"update{model}", self.__build_update_func(model)),
                (f"delete{model}", self.__build_delete_func(model))
            ]:
                _mutation_methods[model] = strawberry.field(
                    resolver=func, name=model)

            _models.popleft()

        for enum_k, enum_v in self._enums.items():
            _mutation_methods[enum_k] = enum_v

        return _mutation_methods

    def __create(self, model: str) -> Type:
        """Create the create input for the given model"""
        _fields = []
        _model_hint = self._models[model] if model in self._models else self._enums[model]
        # Start to iterate over each hint of the model
        for attr, hint in _model_hint.__annotations__.items():
            _type: Any = None
            # define a bool that decides that THIS is not an optional input
            is_optional: bool = False
            if capitalize(attr) in self._enums:
                _type = self._enums[capitalize(attr)]
            elif get_origin(hint) == Union:
                hint_args = get_args(hint)
                # We do not want any forwarded model in the create
                if is_annotated(hint_args[0]) or is_list(hint):
                    continue
                _type = hint_args[0]
                is_optional = type(None) in hint_args
            else:
                # If it's not a enum or a Union, then just return that hint
                _type = hint
            # Append it to the fields
            if is_optional:
                _type = Optional[_type]

            _fields.append((attr, _type, strawberry.UNSET))

        return strawberry.input(make_dataclass(cls_name='create'+model,
                                               fields=_fields))

    def __update(self, model: str) -> Type:
        """Create the update input for the given model"""
        _fields = []
        _model_hint = self._models[model] if model in self._models else self._enums[model]
        # Start to iterate over each hint of the model
        for attr, hint in _model_hint.__annotations__.items():
            _type: Any = None
            # define a bool that decides that THIS is not an optional input
            is_optional: bool = False
            if capitalize(attr) in self._enums:
                _type = self._enums[capitalize(attr)]
            elif get_origin(hint) == Union:
                hint_args = get_args(hint)
                # We do not want any forwarded model in the create
                if is_annotated(hint_args[0]) or is_list(hint):
                    continue
                _type = hint_args[0]
                is_optional = type(None) in hint_args
            else:
                # If it's not a enum or a Union, then just return that hint
                _type = hint
            if is_optional:
                _type = Optional[_type]
            # Append it to the fields
            _fields.append((attr, _type, strawberry.UNSET))

        return strawberry.input(make_dataclass(cls_name='update'+model,
                                               fields=_fields))

    def __build_create_func(self, model: str) -> Callable:
        """Method to generate the create function for each model"""
        response_model = response_by_model[model]

        async def _mutation_function(
            info: strawberry.Info[FastAPIContext],
            element: Type,
        ) -> Response:  # pylint: disable=W0622
            """Function to perform the given mutation"""
            if info.context.authenticated is False:
                raise Error(message="Token or authorization not valid.",
                            status="500",
                            field="token"
                            )
            msg, success, response = self._mutation_utils.create(
                model, model_data=element)
            # Build the response model
            return response_model(
                messages=msg,
                successful=success,
                response=response  # type: ignore
            )

        _mutation_function.__name__ = f"create{model}"
        _mutation_function.__doc__ = f"Create function for the {model} model."
        _mutation_function.__annotations__['return'] = response_by_model[model]
        _mutation_function.__annotations__["element"] = self.__create(model)

        return _mutation_function

    def __build_update_func(self, model: str) -> Callable:
        """Method to generate the update function for each model"""
        # Generate the func template
        response_model = response_by_model[model]

        async def _mutation_function(
            info: strawberry.Info[FastAPIContext],
            element: Type,
            find_by: FindBy
        ) -> None:  # pylint: disable=W0622
            """Function to perform the given mutation"""
            if info.context.authenticated is False:
                raise Error(message="Token or authorization not valid.",
                            status="500",
                            field="token"
                            )
            msg, success, response = self._mutation_utils.update(
                model, model_data=element, find_by=find_by)
            # Build the response model
            return response_model(
                messages=msg,
                successful=success,
                response=response  # type: ignore
            )

        _mutation_function.__name__ = f"update{model}"
        _mutation_function.__doc__ = f"Update function for the {model} model."
        _mutation_function.__annotations__['return'] = response_model
        _mutation_function.__annotations__['element'] = self.__update(model)
        _mutation_function.__annotations__['find_by'] = find_by_models[model]

        return _mutation_function

    def __build_delete_func(self, model: str) -> Callable:
        """Method to generate the delete function for each model"""
        async def _mutation_function(
            info: strawberry.Info[FastAPIContext],
            find_by: FindBy
        ) -> Response:
            """Function to perform the given mutation"""
            if info.context.authenticated is False:
                raise Error(message="Token or authorization not valid.",
                            status="500",
                            field="token"
                            )
            msg, success = self._mutation_utils.delete(
                model, find_by=find_by)
            # Build the response model
            return Response(
                messages=msg,
                successful=success
            )

        _mutation_function.__name__ = f"delete{model}"
        _mutation_function.__doc__ = f"Delete function for the {model} model."
        _mutation_function.__annotations__['find_by'] = find_by_models[model]

        return _mutation_function

    def __build_mutation(self, **kwargs) -> None:
        """Method to generate the Mutation type using all the given arguments
        to use it
        """
        all_methods = {}
        for methods in kwargs.values():
            if methods:
                all_methods.update(methods)
        # Include the login method here
        all_methods['login'] = strawberry.field(
            self._mutation_utils.login
        )
        mutation_obj = type('Mutation', (object, ), all_methods)
        self._mutation_obj = strawberry.type(mutation_obj)

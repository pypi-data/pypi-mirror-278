"""
Script to read the last schema Logic file
and create the strawberry_models from it.
"""
# External imports
import os
import re
from enum import Enum
from dataclasses import dataclass, make_dataclass
from collections import deque, defaultdict
from datetime import date, datetime
from typing import (
    List, Dict, Union, Optional,
    Any, Type, TypeVar,
    get_args, get_origin
)
from typing_extensions import Annotated
# Strawberry imports
import strawberry
# Local imports
from pyworkbench.graphql._utils import (
    FindBy, Response, capitalize, is_annotated, is_list
)

T = TypeVar("T")


class ModelsBuilder:  # pylint: disable=R0902
    """Class generator that, from the last schema Logic file, would update
    the Strawberry Models always to keep the most updated version of the
    the schema logic API in our local DB.

    Args:
    ----------------------------------------------------------------
        - schema_file (str): The schema file to use to update the models
    """
    __slots__ = ['_schema_lines', '_scalars', '_build_classes', '_base_class',
                 '_no_data', '_no_data_list', '_defaults', '_pre_models',
                 '_strawberry_models', '_fix_models', '_enums', '_attr_template']

    def __init__(self, schema_file: str) -> None:
        if not isinstance(schema_file, str):
            raise TypeError(
                f"Schema file must be a string. Got {type(schema_file)} instead.")

        # Also, define the GraphQL scalars equivalences
        self._scalars = {
            'ID': strawberry.ID,
            'Boolean': bool,
            'String': str,
            'Int': int,
            'Integer': int,
            'Float': float,
            'Date': date,
            'DateTime': datetime,
            'Text': str,
            'Password': strawberry.Private[str]
        }

        self._defaults = {
            'UNDEFINED': 'FunctionType.UNDEFINED',
            'UNINITIALIZED': 'ProgramStatus.UNINITIALIZED',
            'PENDING': 'PlanStatus.PENDING',
            'LIMITED': 'LotType.LIMITED',
            'true': True,
            'false': False
        }
        self._attr_template = [{'attr': 'ID'}, {'attr': 'CODE'},
                               {'attr': 'NAME'}, {'attr': 'INSERTED_AT'},
                               {'attr': 'UPDATED_AT'}]
        self._build_classes = {
            'type': self.__build_type, 'enum': self.__build_enum}
        # Generate the base class for the types
        self._base_class = strawberry.type(make_dataclass('BaseModel', [  # type: ignore
            ('id', strawberry.ID, strawberry.UNSET),
            ('insertedAt', Optional[datetime], datetime.now()),
            ('updatedAt', Optional[datetime], datetime.now()),
        ]))
        # Add the resolvers field
        self._no_data = lambda: None
        self._no_data_list = lambda: [None]
        # ---------------------------------------------------
        # Initialize some dictionaries to use
        self._pre_models = defaultdict(dataclass)
        self._strawberry_models = defaultdict(int)
        self._fix_models = defaultdict(list)
        self._enums = defaultdict(object)
        # Initialize the _schema_lines
        self._schema_lines = self.__read_schema_file(schema_file)
        # Initialize the _types and enums variables
        self.__build_models(self.__models_data())  # type: ignore

    @staticmethod
    def decapitalize(model: str) -> str:
        """Return a string in Camel format"""
        return model[0].lower() + model[1:]

    @staticmethod
    def capitalize(model: str) -> str:
        """Return a string with the first letter capitalized"""
        return model[0].upper() + model[1:]

    @staticmethod
    def __lazy_type(model_name: str) -> Annotated:
        """Static method to define a lazy type using Annotated and Strawberry.lazy.

        Args:
        ---------------------------------------------------------------
            - model_name (str): The model to be used as the lazy type.
        """
        return Annotated[model_name, strawberry.lazy(  # type: ignore
            "pyworkbench.graphql.models_builder")]

    @property
    def models(self) -> dict:
        """Property that let the developer access to the models dictionary.

        Returns:
        --------------------------------------------------------------
            - All the strawberry_models
        """
        return self._strawberry_models

    @property
    def enums(self) -> dict:
        """Property that let the developer access to the models dictionary.

        Returns:
        --------------------------------------------------------------
            - All the enums models
        """
        return self._enums

    @staticmethod
    def __read_schema_file(schema_file: str) -> List[str]:
        """Method that would read the schema file"""
        with open(schema_file, 'r', encoding="utf-8") as schema:
            return deque(schema.readlines())  # type: ignore

    def __retrieve_attrs(self) -> List[Dict[str, Union[bool, str]]]:
        """Method to obtain the attributes of a given type or enum."""
        # Define some variables to use
        _attrs = []
        # Initialize a while loop to retrieve the attrs
        left_attrs = True
        while left_attrs:
            attr_template = {'attr': '', 'type': None, 'default': strawberry.UNSET,
                             'unique': False, 'change': True}
            attr = self._schema_lines[0].split('#')[0]
            # Check if the _attrs is equal to }. If it is, then break the while loop.
            if '}' in attr:
                left_attrs = False
                continue
            # Check some conditions of the attribute
            if "@unique" in attr:
                attr = attr.split('@')[0]
                attr_template['unique'] = True
            if "@default" in attr:
                attr, default_value = attr.split('@')
                # Obtain the default value
                default_value = re.search(
                    r"value:\W*(\w+)", default_value).group(1)  # type: ignore
                # And check if the default value is true or false. If it is,
                # capitalize it.
                if default_value in self._defaults:
                    default_value = self._defaults[default_value]
                # Storage the value in the attr_template
                attr_template['default'] = default_value
            if ":" in attr:
                attr_type = re.search(
                    r":\W*(\S[A-z]+)", attr).group(1)  # type: ignore
                # Use the dictionary of scalars ONLY if the type is one of the keys
                if attr_type in self._scalars:
                    attr_type = self._scalars[attr_type]
                # Otherwise, check if the attr_type endswith ]. If it has, then...
                elif "[" in attr and "]" in attr:
                    attr_type = f"List[{attr_type}]"
                attr_template['type'] = attr_type
            # At the end, append this attribute to the _attrs list
            attr_template['attr'] = re.search(
                r"(\w+)", attr).group(1)  # type: ignore
            _attrs.append(attr_template)
            self._schema_lines.popleft()  # type: ignore
        # Return the list from this function
        return _attrs

    def __models_data(self) -> dict[str, defaultdict]:
        """Method that, from the schema_lines, will find out how many
        models do we have and how many enums.
        """
        _models = {'type': defaultdict(list),
                   'enum': defaultdict(list)}
        while self._schema_lines:
            # Select the first line in the queue
            schema_line = self._schema_lines[0]
            if schema_line.startswith(('type', 'enum')):
                _model_type = schema_line.split(' ')[0]
                # Obtain the type from the schema
                _model = re.search(_model_type+r"\W*(\w+)",
                                   schema_line).group(1)  # type: ignore
                # Pre-generate the object to avoid errors
                # self._pre_models[_model] = self.__pre_gen_model(_model)
                # Now, pop that line from the queue and obtain the attrs
                self._schema_lines.popleft()  # type: ignore
                _models[_model_type][_model].append(self.__retrieve_attrs())
                if _model_type == 'type':
                    _models['enum'][_model +
                                    'Attributes'].append(self._attr_template)
            # If don't accomplish any of this, erase the line anyway
            self._schema_lines.popleft()  # type: ignore
        # Return the models once everything is finished
        return _models

    def __build_type(
        self,
        model_name: str,
        model_attrs: List[Dict[str, Any]]
    ) -> Type:  # type: ignore
        """Method to generate the strawberry type for a given model name and attributes.

        Args:
        ---------------------------------------------------------------
            - model_name (str): The name of the model to build
            - model_attrs (List[Dict[str, Any]]): The attributes of the model

        Returns:
        ---------------------------------------------------------------
            - The Strawberry.type model ready to be used in the QueryBuilder
        """
        metadata: dict = {}
        models_reference: list = []
        for attr in model_attrs:
            metadata.update({
                attr["attr"]: {
                    "type": type(attr["type"]).__name__,
                    "is_unique": attr["unique"]
                }
            })
            if isinstance(attr['type'], str) and len(attr['type']):
                # Update the metadata
                # Obtain the type using a simple regex pattern
                _type = re.search(
                    r"(\b(?!(?:List\b))[\w]+)", attr['type']).group(1)  # type: ignore
                # Now, define the attrs to be used in the field
                if attr['type'].startswith('List'):
                    new_attrs = {'type': Optional[List[self.__lazy_type(_type)]],
                                 'default': strawberry.field(resolver=self._no_data_list,
                                                             default=strawberry.UNSET)}
                    models_reference.append(
                        {"attr": attr["attr"], "is_iterable": True})
                else:
                    # Update the model to a lazy type
                    new_attrs = {'type': Optional[self.__lazy_type(_type)],
                                 'default': strawberry.field(resolver=self._no_data,
                                                             default=strawberry.UNSET)}
                    # But also, include a new reference attr
                    models_reference.append({
                        "attr": attr["attr"]+"Id",
                        "is_iterable": False
                    })
                    # Append this to the metadata
                    metadata.update({
                        attr["attr"]+"Id": {
                            "type": strawberry.ID,
                            "is_unique": attr["unique"]
                        }
                    })
                # Finally, update the model attrs with this
                attr.update(new_attrs)

        # Add the attributes from the object
        fields = [(a['attr'], Optional[a['type']], a['default']) if not a['unique']  # type: ignore
                  else (a['attr'], a['type'], a['default']) for a in model_attrs]
        if models_reference:
            fields_ref = []
            metadata_ref = {}
            for r in models_reference:
                if r["is_iterable"] is False:
                    fields_ref.append(
                        (r['attr'], Optional[strawberry.ID], strawberry.UNSET)
                    )
                metadata_ref.update({r["attr"]: r})
            # Also, add this to the metadata
            fields += fields_ref
            metadata["references"] = metadata_ref
        # Create the object and add the metadata parameter
        model_type = strawberry.type(
            make_dataclass(
                model_name,
                fields,  # type: ignore
                bases=(self._base_class,)),
            name=model_name
        )
        model_type.__metadata__ = metadata
        return model_type

    @staticmethod
    def __build_enum(
        model_name: str,
        model_attrs: List[Dict[str, Any]]
    ) -> strawberry.enum:  # type: ignore
        """Method to generate the Strawberry enum for a given model name and attributes.

        Args:
        ---------------------------------------------------------------
            - model_name (str): The name of the model to build
            - model_attrs (List[Dict[str, Any]]): The attributes of the model

        Returns:
        ---------------------------------------------------------------
            - The Strawberry.enum model ready to be used in the QueryBuilder
        """
        # Iterate over all the attributes of the model
        fields = [(a['attr'], a['attr']) for a in model_attrs]
        # Return the enum
        return strawberry.enum(Enum(model_name, fields))  # type: ignore

    def __build_models(self, schema_models: dict[str, list]) -> None:
        """Method that would generate the complete list of strawberry models (it can
        be 'type' or 'enum') given a dictionary with this models.

        Args:
        ----------------------------------------------------------------
            - schema_models (defaultdict(list)): Dictionary with the models (type or enum) obtained
                                from read the 'the schema logic.gql' file
        """
        # Now, for each model that we got in the list of models, build the methods
        for model_type, _models in schema_models.items():
            # Initialize the object
            for _model_name, _model_attrs in _models.items():  # type: ignore
                _model_attrs = _model_attrs[0]  # Access to the attrs
                # Now, generate the model. One option for the enum and other for
                # the normal types
                self._strawberry_models[_model_name] = self._build_classes[model_type](  # type: ignore
                    _model_name, _model_attrs)
                if model_type == 'enum':
                    self._enums[_model_name] = self._strawberry_models[_model_name]
        # And just with that! We can get our methods done

# ================================================================= #
#                       ADDITIONAL BUILDING METHODS                 #
# ================================================================= #


def build_find_by_inputs(
    models_dict: dict,
    enums_dict: dict
) -> Dict[str, Type[FindBy]]:
    """Generate a unique findBy for each type.

    Args:
        - models_dict (dict): dictionary with the key of a model and their corresponding
        dataclass for that model
        - enums_dict (dict): dictionary with the key of a ENUM and their corresponding
        dataclass for that ENUM

    Return:
        - A dict with the FindBy method generated for each element
    """
    # Generate a FindBy method for each model in the enum or model dict
    find_by_model: Dict[str, Type[FindBy]] = {}
    # Create an unique dict for all the inputs

    for dict_to_iterate in [models_dict, enums_dict]:
        for model_name, model in dict_to_iterate.items():
            _fields = []
            # Start to iterate over each hint of the model
            for attr, hint in model.__annotations__.items():
                _type = None
                if capitalize(attr) in enums_dict:
                    _type = enums_dict[capitalize(attr)]
                elif get_origin(hint) == Union:
                    hint_args = get_args(hint)
                    # We do not want any forwarded model in the create
                    if is_annotated(hint_args[0]) or is_list(hint):
                        continue
                    _type = hint_args[0]
                else:
                    # If it's not a enum or a Union, then just return that hint
                    _type = hint
                # Append it to the fields
                _fields.append((attr, Optional[_type], strawberry.UNSET))

            find_by_model[model_name] = strawberry.input(
                make_dataclass(cls_name='FindBy'+model_name,
                               fields=_fields,
                               bases=(FindBy,))
            )
    return find_by_model


def build_mutation_responses(models_dict: dict) -> dict[str, Type[Response]]:
    """Based on the given models, build a dictionary that creates the responses for all
    the mutations that we can perform (such as create, update or delete)

    Args:
        models_dict (dict): Models to iterate over and create their own and unique responses

    Returns:
        dict[str, Type[Response]]: Dictionary to get the response model for each model that we have
    """
    response_models: dict[str, Type[Response]] = {}
    # Iterate over all the models that we created, and just
    # build a new dataclass for it
    for model_name, model in models_dict.items():
        response_models[model_name] = strawberry.type(
            make_dataclass(cls_name='Response'+model_name,
                           fields=[
                               (
                                   "response",
                                   Union[model, None],  # type: ignore
                                   strawberry.UNSET
                               )],
                           bases=(Response,))
        )
    return response_models


# # Call it and make it general so everyone can access to it
SCHEMA_PATH: str = os.environ.get("SCHEMA_PATH", "")
if not SCHEMA_PATH:
    raise ValueError("There's no schema available to use in this project." +
                     " To add one, please refer to one of this two options:\n" +
                     "- Add a env variable called `SCHEMA_PATH`\n" +
                     "- In a configuration file, do the following\n"
                     f" {32*'='}\n"+"    from pyworkbench import graphql\n" +
                     "    graphql.SCHEMA_PATH = <YOUR_SCHEMA>\n" + f"{32*'='}"
                     )
MB = ModelsBuilder(SCHEMA_PATH)
models = MB.models
enums = MB.enums
# Also, generate the find_by_models
find_by_models = build_find_by_inputs(models, enums)
response_by_model = build_mutation_responses(models)

# Call each argument and make it a global variable
globals().update(dict(models.items()))
globals().update(dict(enums.items()))

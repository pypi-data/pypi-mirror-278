"""
Develop a Template for all the Database connectors
"""
from typing import Union, Any, Type, Optional
from abc import ABC, abstractmethod
from datetime import datetime
from dateutil import parser
# Local imports
from pyworkbench.graphql._utils import LoginResponse


class DatabaseConnector(ABC):
    """Database connector. Intended to be an interface for all the Database
    connectors
    """
    __slots__ = ["_models"]

    def __init__(self, models: Any, *_args) -> None:
        self._models: Any = models

    @abstractmethod
    async def login(
        self,
        email: str,
        password: str
    ) -> LoginResponse:
        """Login method for the Mutation process"""

    @abstractmethod
    def singular_search(
            self,
            obj_type: str, **kwargs
    ) -> Union[Type, None]:  # type: ignore
        """Method to perform a search around the database to look for data"""

    @abstractmethod
    def plural_search(
            self,
            obj_type: str, **kwargs
    ) -> Union[Type, None]:  # type: ignore
        """Method to perform a search around the database to look for data"""

    @abstractmethod
    def create(
        self,
        obj_type: str, **kwargs
    ) -> tuple[str, bool, Optional[Type]]:
        """Method to create an element in the database"""

    @abstractmethod
    def update(
        self,
        obj_type: str, **kwargs
    ) -> tuple[str, bool, Optional[Type]]:
        """Method to update an element in the database"""

    @abstractmethod
    def delete(
        self,
        obj_type: str, **kwargs
    ) -> tuple[str, bool]:
        """Method to delete an element in the database"""

    @staticmethod
    def method_name(model: str, p: int = 0) -> str:
        """Function method to return a Camel format for the objects

        Args:
            - model (str): The model to use.
            - p (int): 0 for a singular model and 1 for a plural model. Default to 0.

        Returns:
            - Formatted model
        """
        if p:
            if model.endswith('s'):
                return model[0].lower() + model[1:] + 'es'
            return model[0].lower() + model[1:] + 's'
        # If we don't want it to be plural, just return the normal method
        return model[0].lower() + model[1:]

    def _parse_data(self, obj: str, data: list[dict]) -> list:
        """Static method that fills the Strawberry type with the JSON data that we just
        obtained from the query.

        Args:
        --------------------------------------------------------------
            - obj (str): Object type to search and evaluate.
            - kwargs (Dict[str, Any]): Dictionary of elements to search for.
        """
        if not data:  # If you don't have data to send, don't do anything
            return None  # type: ignore
        # -------------------------------
        models_data = []  # Initialize list for the model per data
        for datum in data:
            # Now, obtain all the inputs from the model
            missing_values = {}
            # for attr in self._models[obj].__annotations__:
            #     if attr.endswith("Id"):
            #         # If the value is not NONE, then get that value
            #         if datum[attr] is None:
            #             continue
            #         # Get the full value as query
            #         attr_model_name = attr[:-2]
            #         attr_data = self.singular_search(
            #             capitalize(attr_model_name),
            #             id=datum[attr]
            #         )
            #         # Fill the data in both sides
            #         datum[attr_model_name] = attr_data
            #     if attr in datum:
            #         continue
            #     missing_values[attr] = None
            missing_values = {
                attr: None for attr in self._models[obj].__annotations__ if attr not in datum}
            datum.update(missing_values)

            # # Evaluate the ForwardRef to convert them also in models
            # for _model_name, ref_type in self._models[obj].__annotations__.items():
            #     # Evaluate if this is a union
            #     if get_origin(ref_type) is Union:
            #         # Now, evaluate the parameters inside the Union
            #         print(get_args(get_origin(ref_type)))

            # Give the correct format to the dates in insertedAt and updatedAt
            for val in ['insertedAt', 'updatedAt']:
                if val not in datum:
                    continue
                datum[val] = parser.parse(datum[val]) if isinstance(
                    datum[val], str) else datum[val]
            # Create the model to use
            models_data.append(type(obj, (object, ), datum))
        return models_data

    @staticmethod
    def get_date(as_str: bool = False) -> Union[datetime, str]:
        """Get the current date in datetime or in a string"""
        current_date = datetime.now()
        if as_str is True:
            return current_date.strftime("%Y-%m-%dT%H:%M:%S")
        return current_date

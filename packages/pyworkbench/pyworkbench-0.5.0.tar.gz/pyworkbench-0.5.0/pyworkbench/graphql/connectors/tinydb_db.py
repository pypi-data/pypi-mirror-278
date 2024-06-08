"""
File that contains utils to generate the local graphql API
"""
from types import ModuleType
from typing import List, Union, Dict, Any, Callable, Type
from functools import reduce, partial
# External imports
import tinydb
import strawberry
# Import the Template
from pyworkbench.graphql.connectors.template import DatabaseConnector


class NoData(Exception):
    """Exception to indicate that the search doesn't return any results."""


class InitializeModules: # pylint: disable=R0903
    """Class to initialize all the modules from a
    folder just using the init and a dict as '__all__'"""

    def __init__(self, module: ModuleType, module_dict: Union[str, List[str]]) -> None:
        # First, validate the module dict variable
        if isinstance(module_dict, str):
            module_dict = [module_dict]
        if not all(isinstance(_dict, str) for _dict in module_dict):
            raise ValueError('The module dict variables must be strings.')
        # Now, do the real good function
        module_attrs = module.__dict__  # Module attrs
        for _dict in module_dict:
            vars_to_import = module_attrs.get(_dict)
            if not vars_to_import:
                raise AttributeError(f"The module {module.__name__} doesn't have the dictionary" +
                                     f" '{_dict}'. Please review.")
            # Import everything as a global variable
            globals().update({var: module_attrs[var]for var in vars_to_import})

# -------------------------------------------------------------- #
#           DEFINE THE QUERY AND MUTATION UTILITIES              #
# -------------------------------------------------------------- #


class TinyConnector(DatabaseConnector):
    """Class to help the Strawberry GraphQL object with some utilities.

    Args:
        - db (tinydb.TinyDB): Database to access the data
        - query (tinydb.Query): Query object
    """
    __slots__ = ['_query', '_db', "_search_args"]

    def __init__(self, models: Any, db_path: str = 'test.jsonb') -> None:
        self._db = tinydb.TinyDB(db_path)
        self._query = tinydb.Query()
        self._search_args = self.__function_per_argument()
        # Initialize the models
        super().__init__(models)

    def __function_per_argument(self) -> dict[str, Any]:
        """Don't write anything here yet, still on work"""  # FIXME
        return {'filter': self.__filter, 'exclude': self.__exclude}

    def plural_search(
        self,
        obj_type: str, **kwargs
    ) -> Union[Type, None]:  # type: ignore
        """Method that would search elements of a given object type

        Args:
        --------------------------------------------------------------
            - obj_type (str): The type of object to search for.
            - kwargs (Dict[Str, Any]): Any kind of argument that can be send from a given object.

            This arguments can be the limit of objects to return, orderBy, filter...

        Returns:
        --------------------------------------------------------------
            - data (Union[Type,None]): The data found with the parameters given.
        """
        obj = getattr(self._query, obj_type.lower())  # Obtain the obj
        # Now, check in the kwargs if the user provide some parameter
        search_params = []  # Initialize this empty list
        limit = 1000  # Initialize the limit as 1,000 values
        order_by = None  # Initialize the order_by variable
        for arg, arg_value in kwargs.items():
            if arg_value == strawberry.UNSET:
                continue  # No parameter provided
            if arg == 'limit':  # If the dev provide a limit, use it.
                limit = arg_value
                continue
            if arg == "page":
                continue  # Since we'd not have so much data, pass the info
            if arg == 'order_by':
                order_by = partial(self.__order_by, arg_value)
                continue
            # Use and get the attrs
            search_params += self._search_args[arg](obj, arg_value)
        # Now, perform the search of the object
        if not search_params:
            data = self._db.table(obj_type.lower()).all()
        else:
            data = self._db.search(
                reduce(lambda arg1, arg2: arg1 | arg2, search_params))

        # If we've the order_by attribute, then order the data
        data = order_by(data, obj_type.lower()) if order_by else data
        return self._parse_data(obj_type, data[:limit])  # type: ignore

    def singular_search(
            self,
            obj_type: str, **kwargs
    ) -> Union[Type, None]:  # type: ignore
        """Method to search in the database given an ID
        or some parameters (using the FindBy method).

        Args:
        --------------------------------------------------------------
            - obj_type (str): The type of the object to search for.
            - obj_id (int): The ID of the object to search.

        Returns:
        --------------------------------------------------------------
            - data (Union[Type,None]): The data found with the parameters given.
        """
        obj = getattr(self._query, self.method_name(
            obj_type))  # Obtain the obj
        data = self._db.search(self.__multi_search(obj, kwargs))
        # Now, from each argument obtained from the query, fulfill the model
        return self._parse_data(obj_type, data)

    @staticmethod
    def __multi_search(obj: tinydb.Query, kwargs: Dict[str, Any]) -> Callable:
        """Static method to generate a multi-search query object using reduce
        from functools.

        Args:
        --------------------------------------------------------------
            - obj (tinydb.Query): Query object to search in the DB.
            - kwargs (Dict[str, Any]): Dictionary of elements to search for.
        """
        return reduce(lambda arg1, arg2: arg1 & arg2, [getattr(obj, attr_key) == str(
            attr_value) for attr_key, attr_value in kwargs.items()
            if attr_value not in [strawberry.UNSET, {}, []]])

    @staticmethod
    def __order_by(
        order_by_method: strawberry.input,  # type: ignore
        data: Dict[str, Any], data_key: str
    ) -> Dict[str, Any]:
        """Method to apply the order_by_method coming as a strawberry input.

        Args:
        ----------------------------------------------------------------
            - order_by_method (strawberry.input): OrderBy method with
                the parameters to apply the filter
            - data (Dict[str, Any]): Data to order
            - data_key (str): Key to access to the data

        Returns:
        ----------------------------------------------------------------
            - Return a list of parameters to apply in the search of data
        """
        [[attr_type, attr]] = [
            [attr_type, attr] for attr_type, attr in order_by_method.__dict__.items()
            if not attr == strawberry.UNSET
        ] or [[None, None]]
        # Now, order the data due the attr.value
        _reverse = bool(attr_type == 'desc')
        data = sorted(  # type: ignore
            data,
            key=lambda value: value[data_key][attr.value.lower()], reverse=_reverse)  # type: ignore
        return data

    @staticmethod
    def __filter(
        obj: tinydb.Query,
        filter_method: strawberry.input  # type: ignore
    ) -> List[Callable]:
        """Method to apply the filter_method coming as a strawberry input.

        Args:
        ----------------------------------------------------------------
            - obj (tinydb.Query): Query object
            - filter_method (strawberry.input): Filter method with the 
                parameters to apply the filter

        Returns:
        ----------------------------------------------------------------
            - Return a list of parameters to apply in the search of data
        """
        # Obtain only those useful attributes, those are the ones that are not UNSET
        useful_attrs = {attr_type: attr for attr_type, attr in filter_method.__dict__.items()
                        if not attr == strawberry.UNSET}
        # Now, for each useful_attrs, decide which action we'd take
        query_params = []  # Initialize the query params list
        for param_key, param in useful_attrs.items():
            if isinstance(param, list):
                query_params.append(getattr(obj, param_key[:-1]).any(param))
            else:
                query_params.append(getattr(obj, param_key) == param)
        # At the end, return the query params
        return query_params

    @staticmethod
    def __exclude(
            obj: tinydb.Query,
            exclude_method: strawberry.input  # type: ignore
    ) -> List[Callable]:  # type: ignore
        """Method to apply the exclude_method coming as a strawberry input.

        Args:
        ----------------------------------------------------------------
            - obj (tinydb.Query): Query object
            - exclude_method (strawberry.input): Filter method
            with the parameters to apply the filter

        Returns:
        ----------------------------------------------------------------
            - Return a list of parameters to apply in the search of data
        """
        getattr(obj)  # type: ignore
        print(exclude_method.__dict__)
        # Just pass the function and don't return nothing

    # ================================================================= #
    #                        MUTATION METHODS                           #
    # ================================================================= #

    def create(
        self,
        obj_type: str, **kwargs,
    ) -> None:
        """Method to create an element in the database"""
        raise NotImplementedError(
            "This method `create` hasn't been implemented for TinyDB connector.")

    def update(
        self,
        obj_type: str, **kwargs,
    ) -> None:
        """Method to update an element in the database"""
        raise NotImplementedError(
            "This method `create` hasn't been implemented for TinyDB connector.")

    def delete(
        self,
        obj_type: str, **kwargs,
    ) -> None:
        """Method to delete an element in the database"""
        raise NotImplementedError(
            "This method `create` hasn't been implemented for TinyDB connector.")

    async def login(
        self,
        email: str,
        password: str,
    ) -> None:
        """Method to delete an element in the database"""
        raise NotImplementedError(
            "This method `login` hasn't been implemented for TinyDB connector.")

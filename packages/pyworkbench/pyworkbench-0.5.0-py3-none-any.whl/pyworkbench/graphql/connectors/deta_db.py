"""
Deta Base connector to handle connections with GraphQL
"""
from typing import Any, Union, Type, Optional
from collections import defaultdict
# External imports
import pydash as _py
import strawberry
# Import the Template
from pyworkbench.graphql._utils import (
    FindBy, LoginResponse, UserLoginResponse,
    capitalize, decapitalize
)
from pyworkbench.graphql.connectors.template import DatabaseConnector
from pyworkbench.database_handler import DatabaseHandler
from pyworkbench.jwt_handler import JWTHandler

JWT = JWTHandler()

class DetaConnector(DatabaseConnector):
    """Connector for the Deta Database. It requires to have the following.env variables:
    
    - DB_ACCESS_TOKEN: It's the DB token access
    """
    __slots__ = ["_db", "_base", "_last_id"]

    def __init__(self, models: Any, base: str) -> None:
        # Call the init from DatabaseConnector
        super().__init__(models)
        self._db = DatabaseHandler()
        self._db.connect(base)
        self._last_id: dict[str, int] = {}

    # ================================================================= #
    #                           QUERY METHODS                           #
    # ================================================================= #

    def singular_search(self, obj_type: str, **kwargs) -> Union[Type, None]:
        """Perform a query to Deta Base"""
        # Get the data performing a query
        parsed_data = self.__perform_query(obj_type, **kwargs)
        if parsed_data:
            # Search for their models references
            self.__fill_references(obj_type, parsed_data)
            return parsed_data[0]
        return None

    def plural_search(self, obj_type: str, **kwargs) -> Union[list[Type], None]:
        """Perform a query to Deta Base"""
        # Get the data performing a query
        filter_args = defaultdict(list)
        # Also, ensure that you'll have only the unique elements provided in the filter
        for field, attr in kwargs["filter"].__dict__.items():
            if not attr or attr == strawberry.UNSET:
                continue
            if field.endswith("s"):
                # Ensure that you've the element in the back
                filter_args[field[:-1]] += attr
            else:
                filter_args[field].append(attr)
        # Parse the data
        parsed_data = self.__perform_query(obj_type, **filter_args)
        if parsed_data:
            return self.__fill_references(obj_type, parsed_data)
        return None

    def __perform_query(self, obj_type: str, **kwargs) -> Union[list[Type], None]:
        """Perform a query using arguments to filter it"""
        # Filter the attributes that were passed for this search
        clean_filter_attrs = {attr: val for attr, val in kwargs.items() if val != strawberry.UNSET}
        # Perform the query using the corresponding table
        table_data = self._db.query(data={"table": obj_type})[0]
        if not "data" in table_data or not table_data:
            table_data = {"data": [], "table": obj_type}
        # From here, filter the data inside the table to obtain only the things that you want
        filtered_data = list(filter(
            lambda entry: all(entry[attr] == field or entry[attr] in field
                              for attr, field in clean_filter_attrs.items()),
            table_data["data"]
        ))
        return self._parse_data(obj_type, filtered_data)

    def __perform_light_query(
        self,
        obj_type: str,
        ids: Optional[list[str]] = None,
    ) -> dict:
        """Perform a pure and light query to obtain all the data in a table"""
        table = self._db.query(data={"table": obj_type})[0]
        if ids is not None:
            table["data"] = _py.filter_(
                table["data"],
                lambda x: x["id"] in ids
            )
        return table

    # ================================================================= #
    #                        MUTATION METHODS                           #
    # ================================================================= #

    def create(
        self,
        obj_type: str,
        **kwargs,
    ) -> tuple[str, bool, Optional[Type]]:
        """Method to create an element in the database"""
        # First, search to see if we got the element in the database.
        table_data = self.__perform_light_query(obj_type)
        if not table_data:
            table_data = {"data": [], "table": obj_type}
            table_data["key"] = self._db.create(table_data)
        # If you do not have the last ID, found it
        if obj_type not in self._last_id and len(table_data["data"]) > 0:
            # Get the maximum from the table data
            max_id = max(table_data["data"], key=lambda x: int(x["id"]))
            # Get the newest id and update it
            self._last_id[obj_type] = int(max_id['id'])
        if len(table_data["data"]) < 1:
            self._last_id[obj_type] = 0

        # Fill a new entry for the data element
        required_attrs = self._models[obj_type].__annotations__
        model_metadata = self._models[obj_type].__metadata__
        new_entry: dict = {}
        for attr in required_attrs:
            if attr in kwargs["model_data"].__dict__:
                input_value = kwargs["model_data"].__dict__[attr]
                if model_metadata[attr]["is_unique"] is True:
                    # Search for that element in the parameters that we have
                    coincidence = _py.find(
                        table_data["data"],
                        lambda x: x[attr] == input_value  # pylint: disable=W0640
                    )
                    if coincidence is not None:
                        error_msg = f"The model {obj_type} already has an instance" +\
                            f" using the field {attr} with value {input_value}," +\
                            " which is an unique value."
                        return error_msg, False, None
                new_entry[attr] = input_value if input_value != strawberry.UNSET else None
            else:
                new_entry[attr] = None
        # And set the new ID
        new_id = self._last_id[obj_type] + 1
        self._last_id[obj_type] += 1
        new_entry["id"] = str(new_id)
        # Add the insertedAt and updateAt
        _date = self.get_date(as_str=True)
        new_entry["insertedAt"] = _date
        new_entry["updatedAt"] = _date
        # Update the table with this new entry
        table_data["data"].append(new_entry)
        # Create the element
        self._db.update(table_data)
        return "", True, self._parse_data(obj_type, [new_entry])[0]

    def update(
        self,
        obj_type: str, **kwargs,
    ) -> tuple[str, bool, Optional[Type]]:
        """Method to update an element in the database"""
        result = self.__filter_data(obj_type, kwargs["find_by"])
        if len(result) == 3:
            return result
        filtered_data, table_data = result
        # Now, update the filtered data with the filter elements
        for field, value in kwargs["model_data"].__dict__.items():
            if value == strawberry.UNSET:
                continue
            filtered_data[field] = value
        # If you found filtered data, update the item
        index = next(
            (i for i, d in enumerate(
                table_data["data"]) if d["id"] == filtered_data["id"]),
            None
        )
        # If found the index, that you should to find, update the element
        if index is not None:
            table_data["data"][index] = filtered_data
        # Update the elements
        self._db.update(table_data)
        return "", True, self._parse_data(obj_type, [filtered_data])[0]

    def delete(
        self,
        obj_type: str, **kwargs,
    ) -> tuple[str, bool]:
        """Method to delete an element in the database"""
        result = self.__filter_data(obj_type, kwargs["find_by"])
        if len(result) == 3:
            return result[0], result[1]
        filtered_data, table_data = result
        # If you found filtered data, remove it
        table_data["data"].remove(filtered_data)
        self._db.update(table_data)
        return "", True

    def __filter_data(self, obj_type: str, find_by: FindBy) -> tuple:
        """Filter the data using the FindBy method"""
        # Get the filters from the findBy method
        clean_filter_attrs = {
            attr: val for attr, val in find_by.__dict__.items()
            if val != strawberry.UNSET
        }
        # Now, get the data
        table_data = self.__perform_light_query(obj_type)
        # Search around the data for the model
        filtered_data = _py.find(
            table_data["data"],
            lambda entry: all(entry[attr] == field or entry[attr] in field
                              for attr, field in clean_filter_attrs.items())
        )
        if not filtered_data:
            msg = f"Couldn't found an instance of {obj_type} with the following filters: "
            # Add the filters
            for attr, val in clean_filter_attrs.items():
                msg += f"[{attr}={val}],"
            return msg[:-1], False, None
        return filtered_data, table_data

    # ================================================================= #
    #                         EXTRA METHODS                             #
    # ================================================================= #
    def __fill_references(self, obj_type: str, data: list[type]) -> list[type]:
        """Fill their models references if there's any"""
        references = self._models[obj_type].__metadata__["references"]
        for d in data:
            # Search their references
            for ref, ref_metadata in references.items():
                ref_id = getattr(d, ref)
                if ref_id is None:
                    continue
                if not isinstance(ref_id, list):
                    ref_id = [ref_id]
                # If there's an associated reference, get that
                if ref_metadata["is_iterable"]:
                    ref_table = capitalize(ref[:-1])
                    ref_model_name = ref
                else:
                    ref_table = capitalize(ref[:-2])
                    ref_model_name = ref[:-2]
                # Get the data and the models
                ref_data = self.__perform_light_query(
                    ref_table, ref_id)["data"]
                ref_models = self._parse_data(ref_table, ref_data)
                if not ref_models:
                    continue
                # Now, connect both elements
                for model in ref_models:
                    if ref_metadata["is_iterable"]:
                        setattr(d, ref_model_name, [model])
                    else:
                        setattr(d, ref_model_name, model)
                    setattr(model, decapitalize(obj_type), d)
        return data

    # ================================================================= #
    #                          LOGIN METHODS                            #
    # ================================================================= #
    async def login(
        self,
        email: str,
        password: str
    ) -> LoginResponse:
        """Login method for the Mutation process"""
        # Get the user
        user_table = self._db.query(data={"table": "User"})[0]
        if user_table:
            [user] = _py.filter_(
                user_table["data"],
                lambda x: x["email"] == email
            ) or [None]
        else:
            user = None
        # Evaluate if the password is correct
        # If there's no user... return an error
        if user is None:
            return LoginResponse(
                messages="Something went wrong. We couldn't find the user.",
                successful=False,
                result=None
            )
        # Evaluate if the password is correct
        if user["password"] != password:
            return LoginResponse(
                messages="Invalid credentials.",
                successful=False,
                result=None
            )
        # If there's a user, return it as response
        # Print the token
        return LoginResponse(
            messages=None,
            successful=True,
            result=UserLoginResponse(
                token=JWT.encode(user)
            )
        )

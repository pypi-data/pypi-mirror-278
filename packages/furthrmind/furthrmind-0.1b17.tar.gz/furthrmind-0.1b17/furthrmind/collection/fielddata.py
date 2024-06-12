from datetime import datetime, date

from bson import ObjectId
from typing_extensions import List, TYPE_CHECKING

from furthrmind.collection.baseclass import BaseClass
from furthrmind.utils import instance_overload

if TYPE_CHECKING:
    from furthrmind.collection.unit import Unit


class FieldData(BaseClass):
    id = ""
    field_name = ""
    field_id = ""
    field_type = ""
    si_value = None
    unit: List["Unit"] = None
    author = None
    value = None

    _attr_definition = {
        "unit": {"class": "Unit"},
        "field_name": {"data_key": "fieldname"},
        "field_type": {"data_key": "fieldtype"},
        "field_id": {"data_key": "fieldid"},
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

        # create instance methods for certain class_methods
        instance_methods = ["_check_value_type"]
        instance_overload(self, instance_methods)

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/fielddata"
        return url

    @classmethod
    def get(cls, id=None):
        raise TypeError("Not implemented")

    @classmethod
    def get_all(cls, project_id=None):
        raise TypeError("Not implemented")

    def update_value(self, value):
        """
        Method to update the value of fielddata

        :param value:
            - Numeric: float or int, or a string convertable to a float
            - Date: datetime, or date object, or unix timestamp or string with iso format
            - SingleLine: string
            - ComboBoxEntry: dict with id or name as key, or string with name, or string with id
            - MultiLine: dict with content as key, or string
            - CheckBox: boolean
        :return: id
        """
        value = self.__class__._check_value_type(value, self.field_type)
        data = {"id": self.id,
                "value": value}
        id = self.post(data)
        self.value = value
        return id

    def set_calculation_result(self, value: dict):
        """
        Method to set a calculation result
        :param value: dict
        :return: id
        """
        if not self.field_type in ["Calculation", "RawDataCalc"]:
            raise TypeError("Only applicable for calculation field")

        url = f"{self.fm.base_url}/set-result/{self.id}"
        response = self.fm.session.post(url, json=value)
        if response.status_code != 200:
            raise ValueError("Setting calculation result failed")
        return self.id

    @classmethod
    def _check_value_type(cls, value, fieldtype=None):
        if value is None:
            return value
        if issubclass(cls, BaseClass):
            # classmethod
            if fieldtype is None:
                raise ValueError("fieldtype must not be None")
        else:
            # instance method
            self = cls
            fieldtype = self.fieldtype
        if fieldtype == "Numeric":
            try:
                value = float(value)
            except:
                raise TypeError("Not numeric")
            return value
        elif fieldtype == "Date":
            if isinstance(value, datetime):
                return int(value.timestamp())
            if isinstance(value, date):
                value = datetime.combine(value, datetime.min.time())
                return int(value.timestamp())
            if isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                    return int(value.timestamp())
                except ValueError:
                    raise TypeError("No iso time format")
            if isinstance(value, (int, float)):
                return value
        elif fieldtype == "SingleLine":
            if isinstance(value, str):
                return value
            if isinstance(value, (float, int)):
                return str(value)
            raise TypeError("Type must be string")

        elif fieldtype == "ComboBoxEntry":
            if isinstance(value, dict):
                if "id" in value:
                    return value
                if "name" in value:
                    return value
                raise TypeError("The dict must have either id or name key")
            if isinstance(value, str):
                try:
                    value = ObjectId(value)
                    value = {"id": value}
                except:
                    value = {"name": value}
                return value
            raise TypeError("Only string and dict supported")

        elif fieldtype == "MultiLine":
            if isinstance(value, dict):
                if "content" not in value:
                    raise TypeError("Key 'content' is required")
                return value
            if isinstance(value, str):
                value = {"content": value}
                return value
            raise TypeError("Only string and dict supported")

        elif fieldtype == "CheckBox":
            if not isinstance(value, bool):
                raise TypeError("value must be a bool")
            return value

    def update_unit(self, unit):
        """
        Method to update the unit of fielddata

        :param unit:
            - dict with id or name, or name as string, or id as string
        :return: id
        """
        unit = self._check_unit(unit)
        data = {"id": self.id,
                "unit": unit}
        id = self.post(data)
        self.unit = unit
        return id

    @classmethod
    def _check_unit(cls, unit):
        if not unit:
            return unit
        if isinstance(unit, dict):
            if "id" in unit:
                return unit
            if "name" in unit:
                return unit
            raise TypeError("The dict must have either id or name key")

        elif isinstance(unit, str):
            try:
                unit = ObjectId(unit)
                unit = {"id": unit}
            except:
                unit = {"name": unit}
            return unit
        raise TypeError("Only string and dict supported")

    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, field_name, field_type, field_id, value, unit, project_id=None):
        """
        Method to create a new fielddata

        :param field_name: name of the field. Either field name and field_type must be specified, or field_id
                           must be specified
        :param field_type: type of the field. Must be out of:
            - Numeric
            - Date
            - SingleLine
            - ComboBoxEntry
            - MultiLine
            - CheckBox
            - Calculation
        :param field_id: id of the field
        :param value:
            - Numeric: float or int, or a string convertable to a float
            - Date: datetime, or date object, or unix timestamp or string with iso format
            - SingleLine: string
            - ComboBoxEntry: dict with id or name as key, or string with name, or string with id
            - MultiLine: dict with content as key, or string
            - CheckBox: boolean
        :param unit: dict with id or name, or name as string, or id as string
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: instance of fielddata class
        """
        from furthrmind.collection import Field

        if field_id:
            data = {"fieldid": field_id}
            field = Field.get(id=field_id)
            field_type = field.type
        else:
            if not field_name or not field_type:
                raise ValueError("fieldname and fieldtype must be specified")
            data = {"fieldname": field_name,
                    "fieldtype": field_type}

        value = FieldData._check_value_type(value, field_type)
        data["value"] = value

        if unit:
            unit = FieldData._check_unit(unit)
            data["unit"] = unit

        id = FieldData.post(data, project_id)
        data["id"] = id
        return data

    @classmethod
    @BaseClass._create_instances_decorator
    def create_many(cls, data_list, project_id=None):
        """
        Method to create many new fielddata

        :param data_list: List with dicts with the following kneys:
        - field_name: name of the field. Either field name and field_type must be specified, or field_id
            must be specified
        -  field_type: type of the field. Must be out of:
            - Numeric
            - Date
            - SingleLine
            - ComboBoxEntry
            - MultiLine
            - CheckBox
            - Calculation

        - field_id: id of the field
        - value:
            - Numeric: float or int, or a string convertable to a float
            - Date: datetime, or date object, or unix timestamp or string with iso format
            - SingleLine: string
            - ComboBoxEntry: dict with id or name as key, or string with name, or string with id
            - MultiLine: dict with content as key, or string
            - CheckBox: boolean

        - unit: dict with id or name, or name as string, or id as string

        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: list with instances of fielddata class

        """

        from furthrmind.collection import Field

        post_data_list = []
        for data in data_list:
            field_id = data.get("field_id")
            field_name = data.get("field_name")
            field_type = data.get("field_type")
            value = data.get("value")
            unit = data.get("unit")

            if field_id:
                _data = {"fieldid": field_id}
                field = Field(id=field_id)
                field.get()
                field_type = field.type
            else:
                if not field_name or not field_type:
                    raise ValueError("field_name and field_type must be specified")
                _data = {"fieldname": field_name,
                         "fieldtype": field_type}

            value = FieldData._check_value_type(value, field_type)
            _data["value"] = value

            if unit:
                unit = FieldData._check_unit(unit)
                _data["unit"] = unit
            post_data_list.append(_data)

        id_list = FieldData.post(post_data_list, project_id)
        for data, id in zip(data_list, id_list):
            data["id"] = id
        return data_list

from furthrmind.collection.baseclass import BaseClassWithFieldData, BaseClass
from typing_extensions import List, Self, Dict, TYPE_CHECKING
from inspect import isclass
if TYPE_CHECKING:
    from furthrmind.collection import *

class ComboBoxEntry(BaseClassWithFieldData):
    id = ""
    name = ""
    files: List["File"] = []
    fielddata: List["FieldData"] = []

    _attr_definition = {
        "files": {"class": "File"},
        "fielddata": {"class": "FieldData"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = ComboBoxEntry.fm.get_project_url(project_id)
        url = f"{project_url}/comboboxentry/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/comboboxentry/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/comboboxentry"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/comboboxentry"
        return url

    @classmethod
    def get(cls, id=None, project_id=None) -> Self:
        """
        Method to get all one comboboxentry by its id
        If called on an instance of the class, the id of the class is used
        :param str id: id of requested comboboxentry
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return Self: Instance of comboboxentry class
        """
        if isclass(cls):
            assert id, "id must be specified"
            return cls._get_class_method(id, project_id=project_id)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), project_id=None) -> List[
        Self]:
        """
        Method to get many comboboxentries belonging to one project
        :param List[str] ids: List with ids
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of experiment class
        """
        assert ids, "ids must be specified"
        return super().get_many(ids, project_id=project_id)
    
    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all comboboxentries belonging to one project
        :param str project_id: Optionally to get comboboxentries from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of comboboxentry class
        """
        return super().get_all(project_id)
    
    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, name: str, field_name: str = None, field_id=None, project_id=None) -> Self:
        """
        Method to create a new combobox entry

        :param name: name of the combobox entry
        :param field_name: Name of the field, where the combobox entry should belong to. Either the field name or id
           must be provided
        :param field_id: id of the field, where the combobox entry should belong to. Either the field name or id must
            be provided
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: instance of column comboboxentry class

        """
        if not name:
            raise ValueError("Name must be specified")
        if not field_name and not field_id:
            raise ValueError("Either field_name or field_id must be provided")

        if field_name:
            fields = Field.get_all(project_id)
            for field in fields:
                if field.name == field_name:
                    field_id = field.id
                    break

            if not field_id:
                raise ValueError("Field with given name not found")

        data = {"name": name, "field": {"id": field_id}}
        id = cls.post(data, project_id)
        data["id"] = id
        return data

    @classmethod
    @BaseClass._create_instances_decorator
    def create_many(cls, data_list: List[Dict], project_id=None) -> Self:
        """
        Method to create a new data column

        :param data_list: dict with the following keys:
            - name of the combobox entry
            - field_name: Name of the field, where the combobox entry should belong to. Either the field name or id
            must be provided
            - field_id: id of the field, where the combobox entry should belong to. Either the field name or id must
            be provided
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: List with instances of comboboxentry class

        """

        look_for_field_ids = False
        for data in data_list:
            if not data.get("name"):
                raise ValueError("Name must be specified")

            if data.get("field_name"):
                look_for_field_ids = True
                break

        if look_for_field_ids:
            fields = Field.get_all(project_id)
            for data in data_list:
                field_name = data.get("field_name")
                field_id = data.get("field_id")
                if not field_name and not field_id:
                    raise ValueError("Either field_name or field_id must be provided")
                if field_name:
                    for field in fields:
                        if field.name == field_name:
                            field_id = field.id
                            data["field_id"] = field_id
                            break
                        if not data.get("field_id"):
                            raise ValueError(f"Field with given name '{field_name}' not found")

        new_data_list = []
        for data in data_list:
            new_data_list.append({
                "name": data.get("name"),
                "field": {"id": data.get("field_id")}
            })

        id_list = cls.post(new_data_list, project_id)
        for data, id in zip(new_data_list, id_list):
            data["id"] = id

        return new_data_list




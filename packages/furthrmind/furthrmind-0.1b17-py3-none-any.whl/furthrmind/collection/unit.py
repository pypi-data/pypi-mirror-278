from furthrmind.collection.baseclass import BaseClass
from typing_extensions import Self, List
from inspect import isclass

class Unit(BaseClass):
    id = ""
    name = ""
    longname = ""
    definition = ""

    _attr_definition = {
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = Unit.fm.get_project_url(project_id)
        url = f"{project_url}/units/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/units/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/units"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/units"
        return url
    
    @classmethod
    def get(cls, id=None) -> Self:
        """
        Method to get all one unit by it's id
        If called on an instance of the class, the id of the class is used
        :param str id: id of requested category 
        :return Self: Instance of unit class
        """

        if isclass(cls):
            assert id, "id must be specified"
            return cls._get_class_method(id)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), project_id=None) -> List[
        Self]:
        """
        Method to get many units belonging to one project
        :param List[str] ids: List with ids
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of experiment class
        """
        return super().get_many(ids, project_id=project_id)

    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all units belonging to one project
        :param str project_id: Optionally to get units from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of unit class
        """
        return super().get_all(project_id)

    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, name: str, definition: str = None, project_id=None) -> Self:
        """
        Method to create a new unit

        :param name: name of the new unit
        :param definition: Unit definition in SI units to convert the new unit to an SI Value. E.g. for unit cm², the
           definition would be: 'cm * cm'. For valid units please check the webapp, open the unit editor.
           You will find there a list of valid units. A definition can als contain scalar values.
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with

        :return: instance of the unit class
        """

        if not name:
            raise ValueError("Name is required")

        data = {"name": name, "definition": definition}
        id = cls.post(data, project_id)
        data["id"] = id
        return data

    @classmethod
    @BaseClass._create_instances_decorator
    def create_many(cls, data_list, project_id=None) -> Self:
        """
        Method to create a new unit

        :param data_list: List of dictionaries with the following keys:
        - name: name of the new unit
        - definition: Unit definition in SI units to convert the new unit to an SI Value. E.g. for unit cm², the
           definition would be: 'cm * cm'. For valid units please check the webapp, open the unit editor.
           You will find there a list of valid units. A definition can als contain scalar values.
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with

        :return: instance of the unit class

        """

        new_data_list = []
        for data in data_list:
            name = data.get("name")
            definition = data.get("definition")
            if not name:
                raise ValueError("Name is required")

            data = {"name": name, "definition": definition}
            new_data_list.append(data)

        id_list = cls.post(new_data_list, project_id)
        for data, id in zip(new_data_list, id_list):
            data["id"] = id

        return new_data_list




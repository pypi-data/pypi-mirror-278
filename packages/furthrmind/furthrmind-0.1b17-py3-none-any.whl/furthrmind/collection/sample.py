from inspect import isclass

from typing_extensions import Self, Dict, List, TYPE_CHECKING

from furthrmind.collection.baseclass import (BaseClassWithFieldData, BaseClassWithFiles,
                                             BaseClassWithGroup, BaseClass,
                                             BaseClassWithLinking)
from furthrmind.utils import instance_overload

if TYPE_CHECKING:
    from furthrmind.collection import *


class Sample(BaseClassWithFieldData,
             BaseClassWithFiles, BaseClassWithGroup,
             BaseClassWithLinking, BaseClass):
    id = ""
    name = ""
    neglect = False
    shortid = ""
    files: List["File"] = []
    fielddata: List["FieldData"] = []
    linked_experiments: List["Experiment"] = []
    linked_samples: List[Self] = []
    linked_researchitems: Dict[str, List["ResearchItem"]] = {}
    groups: List["Group"] = []
    datatables: List["DataTable"] = []

    _attr_definition = {
        "files": {"class": "File"},
        "fielddata": {"class": "FieldData"},
        "groups": {"class": "Group"},
        "linked_samples": {"class": "Sample"},
        "linked_experiments": {"class": "Experiment"},
        "linked_researchitems": {"class": "ResearchItem", "nested_dict": True},
        "datatables": {"class": "DataTable"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)
        # create instance methods for certain class_methods
        instance_methods = ["get"]
        instance_overload(self, instance_methods)

    def _get_url_instance(self, project_id=None):
        project_url = Sample.fm.get_project_url(project_id)
        url = f"{project_url}/samples/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/samples/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/samples"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/samples"
        return url

    @classmethod
    def get(cls, id: str = None, name: str = None, shortid: str = None, project_id: str = None) -> Self:
        """
        Method to get all one sample by its id or short_id
        If called on an instance of the class, the id of the class is used
        :param str id: id or short_id of requested sample 
        :param str name: name of requested sample
        :param str shortid: shortid of requested sample
        :param str project_id: Optionally to get samples from another project as the furthrmind sdk was initiated with, defaults to None
        :return Self: Instance of sample class
        """

        if isclass(cls):
            assert id or name or shortid, "Either id or name must be specified"
            return cls._get_class_method(id, shortid, name, project_id=project_id)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), shortids: List[str] = (), names: List[str] = (), project_id: str = None) -> List[
        Self]:
        """
        Method to get all sample belonging to one project
        :param List[str] ids: List with ids
        :param List[str] shortids: List with short_ids
        :param List[str] names: List with names
        :param str project_id: Optionally to get samples from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of sample class
        """
        assert ids or names or shortids, "Either ids, shortids, or names must be specified"
        return super().get_many(ids, shortids, names, project_id=project_id)

    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all samples belonging to one project
        :param str project_id: Optionally to get samples from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of sample class
        """
        return super().get_all(project_id)

    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, name, group_name=None, group_id=None, project_id=None) -> Self:
        """
        Method to create a new sample

        :param name: the name of the item to be created
        :param group_name: The name of the group where the new item will belong to. group name can be only considered
            for groups that are not subgroups. Either group_name or group_id must be specified
        :param group_id: the id of the group where the new item will belong to. Either group_name or group_id must be specified
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return instance of the sample class

        """

        return Sample._create(name, group_name, group_id, project_id)

    @classmethod
    @BaseClass._create_instances_decorator
    def create_many(cls, data_list: List[Dict], project_id=None) -> Self:
        """
        Method to create multiple samples

        :param data_list: dict with the following keys:
            - name: the name of the item to be created
            - group_name: The name of the group where the new item will belong to. group name can be only considered
            for groups that are not subgroups. Either group_name or group_id must be specified
            - group_id: the id of the group where the new item will belong to. Either group_name or group_id must be specified
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return list with instance of the sample class

        """

        return Sample._create_many(data_list, project_id)

    def add_datatable(self, name: str, columns: List[Dict] = None, project_id=None) -> "DataTable":
        """
        Method to create a new datatable within this sample

        :param name: name of the datatable
        :param columns: a list of columns that should be added to the datatable. List with dicts with the following keys:
            - name: name of the column
            - type: Type of the column, Either "Text" or "Numeric". Data must fit to type, for Text all data
            will be converted to string and for Numeric all data is converted to float (if possible)
            - data: List of column values, must fit to column_type
            - unit: dict with id or name, or name as string, or id as string
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: instance of column datatable class

        """

        from furthrmind.collection import DataTable
        datatable = DataTable.create(name, sample_id=self.id, columns=columns, project_id=project_id)

        new_datatable = list(self.datatables)
        new_datatable.append(datatable)
        self.datatables = new_datatable

        return datatable

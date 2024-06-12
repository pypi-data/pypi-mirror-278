from furthrmind.collection.baseclass import BaseClassWithFieldData, BaseClass
from typing_extensions import List, Dict, Self, TYPE_CHECKING
from inspect import isclass
if TYPE_CHECKING:
    from furthrmind.collection import *


class Group(BaseClassWithFieldData):
    id = ""
    name = ""
    neglect = False
    shortid = ""
    files: List["File"] = []
    fielddata: List["FieldData"] = []
    experiments: List["Experiment"] = []
    samples: List["Sample"] = []
    researchitems: Dict[str, List["ResearchItem"]] = {}
    sub_groups: List[Self] = []
    parent_group: Self = None

    _attr_definition = {
        "files": {"class": "File"},
        "fielddata": {"class": "FieldData"},
        "samples": {"class": "Sample"},
        "experiments": {"class": "Experiment"},
        "researchitems": {"class": "ResearchItem", "nested_dict": True},
        "sub_groups": {"class": "Group"},
        "parent_group": {"class": "Group"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = Group.fm.get_project_url(project_id)
        url = f"{project_url}/groups/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/groups/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/groups"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/groups"
        return url

    @classmethod
    def get(cls, id=None, name=None, shortid=None, parent_group_id=None, project_id=None) -> Self:
        """
        Method to get all one group by its id, name, or shortid
        If called on an instance of the class, the id of the class is used
        :param str id: id or short_id of requested group 
        :param str name: name of requested group
        :param str parent_group_id: id of parent group, If a subgroup is requested, either parent_group_name or parent_group_id is required
        :param shortid: shortid of requested group
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return Self: Instance of group class
        """
        if isclass(cls):
            assert id or name or shortid, "Either id or name must be specified"
            return cls._get_class_method(id, shortid, name, parent_group_id=parent_group_id, project_id=project_id)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), shortids: List[str] = (), names: List[str] = (), project_id=None) -> List[
        Self]:
        """
        Method to get many groups belonging to one project
        :param List[str] ids: List with ids
        :param List[str] shortids: List with short_ids
        :param List[str] names: List names
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of group class
        """
        assert ids or names or shortids, "Either ids, shortids, or names must be specified"
        return super().get_many(ids, shortids, names, project_id=project_id)

    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all groups belonging to one project
        :param str project_id: Optionally to get groups from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of group class
        """
        return super().get_all(project_id)
    
    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, name, parent_group_id=None, project_id=None) -> Self:
        """
        Method to create a new sample
        :param name: the name of the item to be created
        :param parent_group_id: the id of the parent_group, where the new group should belong to
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return instance of the group class
        """
        data = {"name": name}
        if parent_group_id:
            data["parent_group"] = {"id": parent_group_id}
        id = cls.post(data, project_id)
        data["id"] = id
        return data

    @classmethod
    @BaseClass._create_instances_decorator
    def create_many(cls, name_list: List[str], project_id=None) -> List[Self]:
        """
        Method to create multiple groups
        :param name_list: list with names of the groups to be created
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return list with instance of the group class
        """
        data_list = [{"name": name} for name in name_list]

        id_list = cls.post(data_list, project_id)

        for data, id in zip(data_list, id_list):
            data["id"] = id

        return data_list



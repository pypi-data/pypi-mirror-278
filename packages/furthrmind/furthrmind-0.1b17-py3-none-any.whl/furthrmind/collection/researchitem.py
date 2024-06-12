from ..utils import furthr_wrap
from furthrmind.collection.baseclass import (BaseClassWithFieldData, BaseClassWithFiles,
                                             BaseClassWithGroup, BaseClass,
                                             BaseClassWithLinking)
from typing_extensions import List, Dict, Self, TYPE_CHECKING
from inspect import isclass

if TYPE_CHECKING:
    from furthrmind.collection import *

class ResearchItem(BaseClassWithFieldData, BaseClassWithFiles, BaseClassWithGroup, BaseClassWithLinking, BaseClass ):
    id = ""
    name = ""
    neglect = False
    shortid = ""
    files: List["File"] = []
    fielddata: List["FieldData"] = []
    linked_experiments: List["Experiment"] = []
    linked_samples: List["Sample"] = []
    linked_researchitems: Dict[str, List["ResearchItem"]] = {}
    groups: List["Group"] = []
    category: "Category" = None
    datatables: List["DataTable"] = []

    _attr_definition = {
        "files": {"class": "File"},
        "fielddata": {"class": "FieldData"},
        "groups": {"class": "Group"},
        "linked_samples": {"class": "Sample"},
        "linked_experiments": {"class": "Experiment"},
        "linked_researchitems": {"class": "ResearchItem", "nested_dict": True},
        "datatables": {"class": "DataTable"},
        "category": {"class": "Category"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = ResearchItem.fm.get_project_url(project_id)
        url = f"{project_url}/researchitems/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchitems/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchitems"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchitems"
        return url
    
    @classmethod
    def get(cls, id=None, shortid=None, name=None, category_name=None, category_id=None, project_id=None) -> Self:
        """
        Method to get all one researchitem by its id or short_id
        If called on an instance of the class, the id of the class is used
        :param str id: id or short_id of requested researchitem
        :param str shortid: shortid of requested researchitem
        :param str name: name of requested researchitem
        :param str category_name: name of category the research item belongs to
        :param str category_id: id of category the research item belongs to
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return Self: Instance of researchitem class
        """
        assert id or shortid or name, AssertionError("Either id, shortid or name must be given")
        if name:
            assert category_name or category_id, AssertionError("Either category name or id must be given")
        if isclass(cls):
            return cls._get_class_method(id=id, shortid=shortid, name=name,
                                         category_name=category_name, category_id=category_id)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), shortids: List[str] = (), names: List[str] = (),
                 category_name=None, category_id=None, project_id=None) -> List[
        Self]:
        """
        Method to get all experiment belonging to one project
        :param List[str] ids: List with ids
        :param List[str] shortids: List with short_ids
        :param List[str] names: List names
        :param str category_name: name of category the research item belongs to
        :param str category_id: id of category the research item belongs to
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of experiment class
        """
        return cls._get_many(ids, shortids, names, category_name, category_id, project_id=project_id)

    @classmethod
    def _get_many(cls, ids, shortids, names, category_name, category_id, project_id=None):
        assert ids or shortids or names, AssertionError("Either id, shortid or name must be given")
        if names:
            assert category_name or category_id, AssertionError("Either category name or id must be given")
        return super().get_many(ids, shortids, names, category_name, category_id, project_id=project_id)

    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all researchitems belonging to one project
        :param str project_id: Optionally to get researchitems from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of researchitem class
        """
        return super().get_all(project_id)

    @classmethod
    def get_by_name(cls, name, category_name, project_id=None) -> Self:
        return cls._get_by_name_class_method(name, category_name, project_id)

    @classmethod
    def _get_by_name_class_method(cls, name, category_name, project_id):
        all_data = cls.get_all(project_id)
        for d in all_data:
            if d.category.name.lower() == category_name.lower():
                if d.name.lower() == name.lower():
                    return d
        
        raise ValueError("No item with this name found")

    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls,name, group_name = None, group_id=None, category_name=None, category_id = None, project_id=None) -> Self:
        """
        Method to create a new researchitem

        :param name: the name of the item to be created
        :param group_name: The name of the group where the new item will belong to. group name can be only considered
            for groups that are not subgroups. Either group_name or group_id must be specified
        :param group_id: the id of the group where the new item will belong to. Either group_name or group_id must be specified
        :category_name: the name of the category that the new item will belong to. Either category_name or category_id must be specified
        :category_id: the id of the category that the new item will belong to. Either category_name or category_id must be specified
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return instance of the researchitem class

        """

        from furthrmind.collection import Category
        if not category_name and not category_id:
            raise ValueError("Either category name or id must be specified")
        data = cls._prepare_data_for_create(name, group_name, group_id, project_id)

        category_dict = {}
        if category_name:
            category_dict["name"] = category_name
        if category_id:
            category_dict["id"] = category_id

        data["category"] = category_dict
        id = cls.post(data, project_id)

        if "id" not in category_dict:
            categories = Category.get_all(project_id)
            for cat in categories:
                if cat.name == category_name:
                    category_dict["id"] = cat.id
                    break

        data["id"] = id
        return data

    @classmethod
    @BaseClass._create_instances_decorator
    def create_many(cls, data_list: List[Dict], project_id=None) -> Self:
        """
        Method to create multiple experiments

        :param data_list: dict with the following keys:
            - name: the name of the item to be created
            - group_name: The name of the group where the new item will belong to. group name can be only considered
            for groups that are not subgroups. Either group_name or group_id must be specified
            - group_id: the id of the group where the new item will belong to. Either group_name or group_id must be specified
            - category_name: the name of the category that the new item will belong to. Either category_name or category_id must be specified
            - category_id: the id of the category that the new item will belong to. Either category_name or category_id must be specified
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return list with instance of the experiment class

        """
        from furthrmind.collection import Group

        new_list = []
        category_id_not_present = False

        for data in data_list:
            category_name = data.get('category_name')
            category_id = data.get('category_id')
            if not category_name and not category_id:
                raise ValueError("Either category name or id must be specified")

            temp_data = cls._prepare_data_for_create(data.get("name"), data.get("group_name"), data.get("group_id"),
                                                     project_id)

            category_dict = {}
            if category_name:
                category_dict["name"] = category_name
            if category_id:
                category_dict["id"] = category_id

            temp_data["category"] = category_dict
            new_list.append(temp_data)
            if not "id" in category_dict:
                category_id_not_present = True

        id_list = cls.post(new_list, project_id)
        category_mapping = {}
        if category_id_not_present:
            categories = Category.get_all(project_id)
            category_mapping = {cat.name: cat for cat in categories}

        for data, id in zip(new_list, id_list):
            data["id"] = id
            if "id" not in data["category"]:
                cat_id = category_mapping.get(data["category"]["name"])
                data["category"]["id"] = cat_id

        return new_list

    def add_datatable(self, name: str, columns: List[Dict], project_id=None ) -> "DataTable":
        """
        Method to create a new datatable within this experiment

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
        datatable = DataTable.create(name, researchitem_id=self.id, columns=columns, project_id=project_id)

        new_datatable = list(self.datatables)
        new_datatable.append(datatable)
        self.datatables = new_datatable

        return datatable


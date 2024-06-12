from furthrmind.collection.baseclass import BaseClass
from typing_extensions import List, Dict, Self, TYPE_CHECKING
from inspect import isclass
if TYPE_CHECKING:
    from furthrmind.collection import *

class Project(BaseClass):
    id = ""
    name = ""
    info = ""
    shortid = ""
    samples: List["Sample"] = []
    experiments: List["Experiment"] = []
    groups: List["Group"] = []
    units: List["Unit"] = []
    researchitems: Dict[str, List["ResearchItem"]] = {}
    permissions = []
    fields: List["Field"] = []

    _attr_definition = {
        "samples": {"class": "Sample"},
        "experiments": {"class": "Experiment"},
        "groups": {"class": "Group"},
        "units": {"class": "Unit"},
        "researchitems": {"class": "ResearchItem", "nested_dict": True},
        "fields": {"class": "Field"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self):
        project_url = self.fm.get_project_url(self.id)
        return project_url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(id)
        return project_url

    @classmethod
    def _get_all_url(cls, project_id=None):
        return f"{cls.fm.base_url}/projects"

    @classmethod
    def _post_url(cls):
        return f"{cls.fm.base_url}/projects"
    
    @classmethod
    def get(cls, id=None, name=None) -> Self:
        """
        Method to get all one project by it's id
        If called on an instance of the class, the id of the class is used
        :param str id: id or short_id of requested project 
        :param str name: name of requested project 
        :return Self: Instance of project class
        """

        if isclass(cls):
            assert id or name, "Either id or name must be specified"
            return cls._get_class_method(id, name=name)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), names: List[str]= ()) -> List[
        Self]:
        """
        Method to get many columns belonging to one project
        :param List[str] ids: List with ids
        :param List[str] names: List names
        :return List[Self]: List with instances of experiment class
        """
        assert ids or names, "Either ids or names must be specified"
        return super().get_many(ids, names)

    @classmethod
    def get_all(cls) -> List[Self]:
        """
        Method to get all projects belonging to one project
        :return List[Self]: List with instances of project class
        """
        return super().get_all()

    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, name: str) -> Self:
        """
        Method to create a new project
        :param name: Name of the new project
        :return: instance of the project class
        """

        if not name:
            raise ValueError("Name is required")
        data = {"name": name}
        id = cls.post(data)
        data["id"] = id
        return data





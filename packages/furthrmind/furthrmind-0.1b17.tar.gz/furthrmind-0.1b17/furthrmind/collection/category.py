from inspect import isclass
from furthrmind.collection.baseclass import BaseClass
from typing_extensions import TYPE_CHECKING, List, Self

class Category(BaseClass):
    id = ""
    name = ""
    description = ""
    project = ""

    _attr_definition = {
        "project": {"class": "Project"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = Category.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory"
        return url

    @classmethod
    def get(cls, id=None, project_id=None) -> Self:
        """
        Method to get all one category by its id
        If called on an instance of the class, the id of the class is used
        :param str id: id of requested category
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return Self: Instance of category class
        """

        if isclass(cls):
            assert id, "id must be specified"
            return cls._get_class_method(id, project_id=project_id)
        else:
            self = cls
            data = self._get_instance_method()
            return data

    @classmethod
    def get_many(cls, ids: List[str] = (), names: List[str] = (), project_id=None) -> List[Self]:
        """
        Method to get many categories belonging to one project
        :param List[str] ids: List with ids
        :param List[str] names: List names
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of experiment class
        """
        assert ids, "ids must be specified"
        return super().get_many(ids, names, project_id=project_id)

    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all categories belonging to one project
        :param str project_id: Optionally to get categories from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of category class
        """
        return super().get_all(project_id)
    
    @staticmethod
    def create(name:str, project_id=None) -> Self:
        """
        Method to create a new category
        :param str name: Name of new category
        :param str project_id: Optionally to create a category in another project as the furthrmind sdk was initiated with, defaults to None
        """
        pass





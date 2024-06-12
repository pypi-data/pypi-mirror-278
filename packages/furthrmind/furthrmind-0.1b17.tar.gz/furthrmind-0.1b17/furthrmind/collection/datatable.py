from ..utils import furthr_wrap
from furthrmind.collection.baseclass import BaseClass
from typing_extensions import Self, List, TYPE_CHECKING
from pandas import DataFrame
from inspect import isclass
if TYPE_CHECKING:
    from furthrmind.collection import Column

class DataTable(BaseClass):
    id = ""
    name = ""
    columns: List["Column"] = []


    _attr_definition = {
        "columns": {"class": "Column"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = DataTable.fm.get_project_url(project_id)
        url = f"{project_url}/rawdata/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/rawdata/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/rawdata"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/rawdata"
        return url
    
    @classmethod
    def get(cls, id=None, project_id=None) -> Self:
        """
        Method to get all one datatable by its id
        If called on an instance of the class, the id of the class is used
        :param str id: id of requested datatable
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return Self: Instance of datatable class
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
        Method to get many datatables belonging to one project
        :param List[str] ids: List with ids
        :param str project_id: Optionally to get experiments from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of experiment class
        """
        assert ids, "ids must be specified"
        return super().get_many(ids, project_id=project_id)

    @classmethod
    def get_all(cls, project_id=None) -> List[Self]:
        """
        Method to get all datatables belonging to one project
        :param str project_id: Optionally to get datatables from another project as the furthrmind sdk was initiated with, defaults to None
        :return List[Self]: List with instances of datatable class
        """
        return super().get_all(project_id)

    def get_columns(self, column_id_list: List[str]=None, column_name_list:List[str]=None) -> List["Column"]:
        """
        Method to get columns and their data
        If column_id_list and column_name_list are not provided, the method will retrieve all columns belonging
        to the datatable

        :param column_id_list: list of column_ids to retrieve
        :param column_name_list: list of column names to retrieve
        :return: list of column objects

        """

        columns = self._get_columns(column_id_list, column_name_list)
        new_column_mapping = {c.id: c for c in columns}
        new_column_list = []
        for column in self.columns:
            if column.id in new_column_mapping:
                new_column_list.append(new_column_mapping[column.id])
            else:
                new_column_list.append(column)
        self.columns = new_column_list
        return columns

    def get_pandas_dataframe(self, column_id_list: List[str]=None, column_name_list:List[str]=None) -> DataFrame:
        """
        Method to get columns and their data as a pandas dataframe
        If column_id_list and column_name_list are not provided, the method will retrieve all columns belonging
        to the datatable

        :param column_id_list: list of column_ids to retrieve
        :param column_name_list: list of column names to retrieve
        :return: pandas dataframe

        """

        columns = self._get_columns(column_id_list, column_name_list)
        data_dict = {}
        for c in columns:
            data_dict[c.name] = c.values
        df = DataFrame.from_dict(data_dict)
        return df

    def _get_columns(self, column_id_list: List[str]=None, column_name_list:List[str]=None) -> List["Column"]:
        from furthrmind.collection import Column
        if column_id_list:
            pass
        elif column_name_list:
            column_id_list = []
            for column in self.columns:
                if column.name in column_name_list:
                    column_id_list.append(column.id)
        else:
            column_id_list = [c.id for c in self.columns]
        columns = Column.get_many(ids=column_id_list)
        return columns

    @classmethod
    @BaseClass._create_instances_decorator
    def create(cls, name: str = "Data table", experiment_id=None, sample_id=None, researchitem_id=None, columns=None, project_id=None) -> Self:
        """
        Method to create a new datatable

        :param name: name of the datatable
        :param experiment_id: id of the experiment where the datatable belongs to
        :param sample_id: id of the sample where the datatable belongs to
        :param researchitem_id: id of the researchitem where the datatable belongs to
        :param columns: a list of columns that should be added to the datatable. List with dicts with the following keys:
            - name: name of the column
            - type: Type of the column, Either "Text" or "Numeric". Data must fit to type, for Text all data
            will be converted to string and for Numeric all data is converted to float (if possible)
            - data: List of column values, must fit to column_type
            - unit: dict with id or name, or name as string, or id as string
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: instance of datatable class

        """

        from furthrmind.collection import Column

        if not name:
            raise ValueError("Name must be specified")

        if not experiment_id and not sample_id and not researchitem_id:
            raise ValueError("Either experiment_id or sample_id or researchitem_id must be specified")

        column_id_list = []
        if columns:
            columns = Column.create_many(columns)
            column_id_list = [c.id for c in columns]

        data = {"name": name}
        if column_id_list:
            data["columns"] = [{"id": column_id} for column_id in column_id_list]

        if experiment_id:
            data["experiment"] = {"id": experiment_id}

        if sample_id:
            data["sample"] = {"id": sample_id}

        if researchitem_id:
            data["researchitem"] = {"id":researchitem_id}

        id = cls.post(data, project_id)
        data["id"] = id
        return data


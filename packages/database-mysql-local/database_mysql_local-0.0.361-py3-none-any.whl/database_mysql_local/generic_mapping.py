from logger_local.MetaLogger import MetaLogger

from .constants import LOGGER_MAPPING_CODE_OBJECT
from .generic_crud import GenericCRUD


class GenericMapping(GenericCRUD, metaclass=MetaLogger, object=LOGGER_MAPPING_CODE_OBJECT):
    def __init__(self, default_schema_name: str = None,
                 default_table_name: str = None,
                 default_view_table_name: str = None,
                 default_view_with_deleted_and_test_data: str = None,
                 default_id_column_name: str = None, default_column_name: str = None,
                 default_entity_name1: str = None,
                 default_entity_name2: str = None,
                 is_test_data: bool = False):
        default_column_name = default_column_name or default_id_column_name
        super().__init__(default_schema_name=default_schema_name,
                         default_table_name=default_table_name, default_view_table_name=default_view_table_name,
                         default_view_with_deleted_and_test_data=default_view_with_deleted_and_test_data,
                         default_column_name=default_column_name, is_test_data=is_test_data)
        self.default_entity_name1 = default_entity_name1
        self.default_entity_name2 = default_entity_name2

    # We added the schema_name parameter to avoid using USE and void creating a new instance/object
    # of the database for mapping.
    def insert_mapping(self, *, entity_id1: int, entity_id2: int,
                       entity_name1: str = None, entity_name2: str = None,
                       schema_name: str = None, data_dict: dict = None, data_json: dict = None,
                       ignore_duplicate: bool = False) -> int:
        """Inserts a new link between two entities and returns the id of the
          new row or -1 if an error occurred.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param schema_name: The name of the schema.
        :param data_dict: The data to insert.
        :param ignore_duplicate: If True, ignore duplicate rows.
        :return: The id of the new row or -1 if an error occurred.
        """
        data_dict = data_dict or self._data_json_to_dict(data_json)
        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        schema_name = schema_name or self.default_schema_name
        table_name = f"{entity_name1}_{entity_name2}_table"
        data_dict = data_dict or {}
        data_dict[f"{entity_name1}_id"] = entity_id1
        data_dict[f"{entity_name2}_id"] = entity_id2
        mapping_id = super().insert(schema_name=schema_name, data_dict=data_dict, table_name=table_name,
                                    ignore_duplicate=ignore_duplicate)
        return mapping_id

    def insert_mapping_if_not_exists(self, *, entity_id1: int, entity_id2: int,
                                     entity_name1: str = None, entity_name2: str = None,
                                     schema_name: str = None, data_dict: dict = None,
                                     view_table_name: str = None) -> int:
        """Inserts a new link between two entities if it does not exist and returns the id of the
            new row or -1 if an error occurred.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param schema_name: The name of the schema.
        :param data_dict: The data to insert.
        :return: The id of the new row or -1 if an error occurred.
        """
        data_dict = data_dict or {}
        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        schema_name = schema_name or self.default_schema_name
        table_name = f"{entity_name1}_{entity_name2}_table"
        view_table_name = view_table_name or f"{entity_name1}_{entity_name2}_view"
        data_dict[f"{entity_name1}_id"] = entity_id1
        data_dict[f"{entity_name2}_id"] = entity_id2
        data_dict_compare = {
            f"{entity_name1}_id": entity_id1,
            f"{entity_name2}_id": entity_id2
        }
        mapping_id = super().insert_if_not_exists(schema_name=schema_name, data_dict=data_dict, table_name=table_name,
                                                  data_dict_compare=data_dict_compare, view_table_name=view_table_name)
        return mapping_id


    def upsert_mapping(self, *, entity_id1: int, entity_id2: int,
                       entity_name1: str = None, entity_name2: str = None,
                       schema_name: str = None, data_dict: dict = None,
                       data_dict_compare: dict = None) -> int:
        """Inserts a new link between two entities and returns the id of the
            new row or -1 if an error occurred.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param schema_name: The name of the schema.
        :param data_dict: The data to insert.
        :return: The id of the new row or -1 if an error occurred.
        """
        data_dict = data_dict or {}
        data_dict_compare = data_dict_compare or {}
        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        schema_name = schema_name or self.default_schema_name
        table_name = f"{entity_name1}_{entity_name2}_table"
        data_dict_compare[f"{entity_name1}_id"] = data_dict[f"{entity_name1}_id"] = entity_id1
        data_dict_compare[f"{entity_name2}_id"] = data_dict[f"{entity_name2}_id"] = entity_id2
        mapping_id = super().upsert(schema_name=schema_name, data_dict=data_dict, table_name=table_name)
        return mapping_id


    # TODO: do we need delete_mapping_by_id?
    def delete_mapping_by_two_ids(self, *, entity_id1: int, entity_id2: int,
                                  entity_name1: str = None, entity_name2: str = None,
                                  schema_name: str = None) -> None:
        """ Deletes a link between two entities.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param schema_name: The name of the schema.
        :return: None
        """

        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        schema_name = schema_name or self.default_schema_name
        table_name = f"{entity_name1}_{entity_name2}_table"

        where = f"{entity_name1}_id=%s AND {entity_name2}_id=%s"
        params = (entity_id1, entity_id2)
        super().delete_by_where(schema_name=schema_name, table_name=table_name, where=where, params=params)

    # TODO: remove _by_id, as there's no by_where. Plus, it's by ids. make it backward compatible
    def select_multi_mapping_tuple_by_id(self, *, entity_id1: int, entity_id2: int,
                                         entity_name1: str = None, entity_name2: str = None,
                                         schema_name: str = None, select_clause_value: str = "*") -> list:
        """Selects a row from the database by id.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param schema_name: The name of the schema.
        :param select_clause_value: The columns to select.
        :return: A list of dictionaries representing the rows.
        """
        assert entity_id1 is not None
        assert entity_id2 is not None

        entity_name1 = entity_name1 or self.default_entity_name1
        entity_name2 = entity_name2 or self.default_entity_name2
        schema_name = schema_name or self.default_schema_name
        table_name = f"{entity_name1}_{entity_name2}_view"
        where = f"{entity_name1}_id=%s AND {entity_name2}_id=%s"
        params = (entity_id1, entity_id2)
        result = super().select_multi_tuple_by_where(schema_name=schema_name, view_table_name=table_name,
                                                     select_clause_value=select_clause_value,
                                                     where=where, params=params)
        return result

    def select_multi_mapping_dict_by_id(self, *, entity_id1: int, entity_id2: int,
                                        entity_name1: str = None, entity_name2: str = None,
                                        schema_name: str = None, select_clause_value: str = "*") -> list:
        """Selects a row from the database by id.
        :param entity_name1: The name of the first entity's table.
        :param entity_name2: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :param schema_name: The name of the schema.
        :param select_clause_value: The columns to select.
        :return: A list of dictionaries representing the rows.
        """

        result = self.select_multi_mapping_tuple_by_id(entity_name1=entity_name1, entity_name2=entity_name2,
                                                       entity_id1=entity_id1, entity_id2=entity_id2,
                                                       schema_name=schema_name,
                                                       select_clause_value=select_clause_value)

        result = super().convert_multi_to_dict(result, select_clause_value)
        return result

    # TODO: add select_one_dict/tuple/value, and select_multi_value

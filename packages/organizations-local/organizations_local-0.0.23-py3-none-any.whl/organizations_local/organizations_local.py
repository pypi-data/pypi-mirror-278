from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext

from .organizations_constants import ORGANIZATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

user_context = UserContext()

DEFAULT_SCHEMA_NAME = "organization"
DEFAULT_TABLE_NAME = "organization_table"
DEFAULT_VIEW_NAME = "organization_view"
DEFAULT_ID_COLUMN_NAME = "organization_id"
DEFAULT_ML_TABLE_NAME = "organization_ml_table"
DEFAULT_ML_VIEW_NAME = "organization_ml_view"
DEFAULT_ML_ID_COLUMN_NAME = "organization_ml_id"
DEFAULT_NOT_DELETED_ML_VIEW_NAME = "organization_ml_not_deleted_view"


# "organization_table fields":
#     "number",
#     "identifier",
#     "is_approved",
#     "is_main",
#     "point",
#     "location_id",
#     "profile_id",
#     "parent_organization_id",
#     "non_members_visibility_scope_id",
#     "members_visibility_scope_id",
#     "Non_members_visibility_profile_id",
#     "is_test_data",
#     "created_timestamp",
#     "created_user_id",
#     "created_real_user_id",
#     "created_effective_user_id",
#     "created_effective_profile_id",
#     "updated_timestamp",
#     "updated_user_id",
#     "updated_real_user_id",
#     "updated_effective_user_id",
#     "updated_effective_profile_id",
#     "start_timestamp",
#     "end_timestamp",
#     "main_group_id"
# 
# organization_ml_table fields:
#     "organization_ml_id",
#     "organization_id",
#     "lang_code",
#     "is_main",
#     "name",
#     "is_title_approved",
#     "is_description_approved",
#     "description"


class OrganizationsLocal(GenericCRUDML, metaclass=MetaLogger,
                         object=ORGANIZATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data=False) -> None:
        GenericCRUDML.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                               default_table_name=DEFAULT_TABLE_NAME,
                               default_column_name=DEFAULT_ID_COLUMN_NAME,
                               is_test_data=is_test_data)
        self.default_view_table_name = DEFAULT_VIEW_NAME

    @staticmethod
    def _clean_organization_dict(organization_dict: dict) -> dict:
        columns = ("name", "is_approved", "is_main", "point", "location_id", "profile_id", "parent_organization_id",
                   "non_members_visibility_scope_id", "members_visibility_scope_id",
                   "Non_members_visibility_profile_id", "main_group_id")
        organization_dict = {key: organization_dict.get(key) for key in columns}
        return organization_dict

    @staticmethod
    def _clean_organization_ml_dict(organization_dict: dict) -> dict:
        columns = ("lang_code", "is_main", "title", "is_title_approved",
                   "is_description_approved", "description")
        organization_ml_dict = {key: organization_dict.get(key) for key in columns}
        return organization_ml_dict

    # TODO: rename to insert? same for all
    def insert_organization(self, organization_dict: dict) -> tuple[int, int]:
        # This should be before chaning the organization_dict
        organization_ml_data_dict = self._clean_organization_ml_dict(organization_dict)

        organization_dict = self._clean_organization_dict(organization_dict)
        organization_id = GenericCRUDML.insert(self, data_dict=organization_dict)
        organization_ml_data_dict["organization_id"] = organization_id
        organization_ml_id = GenericCRUDML.insert(self, table_name="organization_ml_table",
                                                  data_dict=organization_ml_data_dict)

        return organization_id, organization_ml_id

    def upsert_organization(self, organization_dict: dict, order_by: str = None) -> dict:
        lang_code = LangCode.detect_lang_code_restricted(text=organization_dict.get('title'), default_lang_code=LangCode.ENGLISH)
        organization_ml_dict = self._clean_organization_ml_dict(organization_dict)
        organization_dict = self._clean_organization_dict(organization_dict)

        if "(" and ")" in organization_dict.get('title', ''):
            organization_id, organzation_ml_ids_list = GenericCRUDML.upsert_value_with_abbreviations(
                self, data_ml_dict=organization_ml_dict, lang_code=lang_code,
                data_dict=organization_dict, schema_name=DEFAULT_SCHEMA_NAME, table_name=DEFAULT_TABLE_NAME,
                ml_table_name=DEFAULT_ML_TABLE_NAME, order_by=order_by)
        else:
            organization_id, organzation_ml_id = GenericCRUDML.upsert_value(
                self, data_ml_dict=organization_ml_dict, lang_code=lang_code,
                data_dict=organization_dict, schema_name=DEFAULT_SCHEMA_NAME, table_name=DEFAULT_TABLE_NAME,
                ml_table_name=DEFAULT_ML_TABLE_NAME, order_by=order_by)
            organzation_ml_ids_list = [organzation_ml_id]

        upsert_information = {
            "organization_id": organization_id,
            "organization_ml_ids_list": organzation_ml_ids_list
        }

        return upsert_information

    def update_organization(self, *, organization_id: int, organization_ml_id: int, organization_dict: dict) -> None:
        # TODO: should we have such method in CRUD ML? same for delete
        organization_ml_dict = self._clean_organization_ml_dict(organization_dict)
        organization_ml_dict["organization_id"] = organization_id
        organization_dict = self._clean_organization_dict(organization_dict)
        GenericCRUDML.update_by_column_and_value(self, column_value=organization_id,
                                                 data_dict=organization_dict)
        GenericCRUDML.update_by_column_and_value(self, table_name="organization_ml_table",
                                                 column_value=organization_ml_id, data_dict=organization_ml_dict,
                                                 column_name="organization_ml_id")

    def get_organization_dict_by_organization_id(
            self, *, organization_id: int, organization_ml_id: int = None, view_table_name: str = None) -> dict:
        view_table_name = view_table_name or self.default_view_table_name
        organization_ml_dict = {}
        if organization_ml_id:
            organization_ml_dict = self.select_one_dict_by_column_and_value(
                view_table_name="organization_ml_view",
                column_value=organization_ml_id, column_name="organization_ml_id")
        organization_dict = self.select_one_dict_by_column_and_value(
            view_table_name=view_table_name,
            column_value=organization_id, column_name="organization_id")

        return {**organization_dict, **organization_ml_dict}

    def get_organizations_names_list_by_organizations_ids(
            self, *, organizations_ids_list: list[int], lang_codes_list: list[LangCode] = None,
            view_table_name: str = None) -> list[str]:
        lang_codes_list = lang_codes_list or [LangCode.ENGLISH]
        view_table_name = view_table_name or DEFAULT_ML_VIEW_NAME
        organizations_names_list = []
        for organization_id in organizations_ids_list:
            organization_name_dicts = self.select_multi_dict_by_column_and_value(
                view_table_name=view_table_name, select_clause_value="title, lang_code",
                column_name="organization_id", column_value=organization_id)

            # filter by lang_codes_list
            # TODO: improve performance
            for lang_code in lang_codes_list:
                for organization_name_dict in organization_name_dicts:
                    if organization_name_dict.get('lang_code') == lang_code.value:
                        organizations_names_list.append(organization_name_dict.get('title'))

        return organizations_names_list

    def delete_by_organization_id(self, organization_id: int, organization_ml_id: int = None) -> None:
        # Delete from organization_table
        self.delete_by_column_and_value(table_name="organization_table",
                                        column_name="organization_id", column_value=organization_id)

        # Delete from organization_ml_table
        if organization_ml_id:
            self.delete_by_column_and_value(table_name="organization_ml_table",
                                            column_name="organization_ml_id", column_value=organization_ml_id)

    def get_test_organization_id(self) -> int:
        test_organization_id = self.get_test_entity_id(
            entity_name="organization", insert_function=self.insert_organization)
        return test_organization_id

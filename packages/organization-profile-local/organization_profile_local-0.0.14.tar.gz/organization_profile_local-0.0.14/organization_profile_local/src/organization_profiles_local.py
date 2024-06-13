from datetime import datetime

from database_mysql_local.generic_mapping import GenericMapping
from logger_local.MetaLogger import MetaLogger

from .organization_profile_constants import ORGANIZATION_PROFILE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

DEFAULT_SCHEMA_NAME = "organization_profile"
DEFAULT_TABLE_NAME = "organization_profile_table"
DEFAULT_VIEW_NAME = "organization_profile_view"
DEFAULT_ID_COLUMN_NAME = "organization_profile_id"
DEFAULT_ENTITY_NAME1 = "organization"
DEFAULT_ENTITY_NAME2 = "profile"


class OrganizationProfilesLocal(GenericMapping, metaclass=MetaLogger,
                                object=ORGANIZATION_PROFILE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False):
        GenericMapping.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                                default_table_name=DEFAULT_TABLE_NAME,
                                default_view_table_name=DEFAULT_VIEW_NAME,
                                default_column_name=DEFAULT_ID_COLUMN_NAME,
                                default_entity_name1=DEFAULT_ENTITY_NAME1,
                                default_entity_name2=DEFAULT_ENTITY_NAME2,
                                is_test_data=is_test_data)

    def insert_mapping(self, organization_id: int, profile_id: int, ignore_duplicate: bool = False) -> int:

        organization_profile_id = GenericMapping.insert_mapping(self, entity_id1=organization_id, entity_id2=profile_id,
                                                                ignore_duplicate=ignore_duplicate)

        return organization_profile_id

    def insert_mapping_if_not_exists(self, organization_id: int, profile_id: int) -> int:

        organization_profile_id = self.get_organization_profile_id(organization_id=organization_id,
                                                                   profile_id=profile_id)
        if organization_profile_id:
            self.logger.info("The link already exists",
                             object={"organization_id": organization_id, "profile_id": profile_id})

            return organization_profile_id
        organization_profile_id = self.insert_mapping(organization_id=organization_id, profile_id=profile_id)

        return organization_profile_id

    def insert_multiple_mappings_if_not_exists(self, organizations_ids: list[int], profiles_ids: list[int]) -> list[
        int]:

        organization_profiles_ids = []
        for organization_id in organizations_ids:
            for profile_id in profiles_ids:
                organization_profile_id = self.insert_mapping_if_not_exists(organization_id=organization_id,
                                                                            profile_id=profile_id)
                organization_profiles_ids.append(organization_profile_id)

        return organization_profiles_ids

    def get_profile_id_and_organization_id(self, organization_profile_id: int) -> dict[str, int]:

        result = self.select_one_dict_by_column_and_value(
            select_clause_value="organization_id, profile_id",
            column_name=DEFAULT_ID_COLUMN_NAME,
            column_value=organization_profile_id
        )

        return result

    def get_linked_profile_ids(self, organization_id: int) -> list[int]:

        profile_ids_tuple_list = self.select_multi_tuple_by_where(
            select_clause_value="profile_id",
            where="organization_id = %s",
            params=(organization_id,)
        )
        profile_ids_list = [profile_id for (profile_id,) in profile_ids_tuple_list]

        return profile_ids_list

    def get_linked_organization_ids(self, profile_id: int) -> list[int]:

        organization_ids_tuple_list = self.select_multi_tuple_by_where(
            select_clause_value="organization_id",
            where="profile_id = %s",
            params=(profile_id,)
        )
        organization_ids_list = [organization_id for (organization_id,) in organization_ids_tuple_list]

        return organization_ids_list

    # get organization ids linked to a profile id with updated_timestamp greater than remote_last_modified_timestamp
    def get_linked_organization_ids_with_updated_timestamp(self, profile_id: int,
                                                           remote_last_modified_timestamp: datetime) -> list[int]:

        organization_ids_tuple_list = self.select_multi_tuple_by_where(
            select_clause_value="organization_id",
            where="profile_id = %s AND updated_timestamp > %s",
            params=(profile_id, remote_last_modified_timestamp)
        )
        organization_ids_list = [organization_id for (organization_id,) in organization_ids_tuple_list]

        return organization_ids_list

    def get_organization_profile_id(self, organization_id: int, profile_id: int) -> int | None:

        organization_profile_id = self.select_one_value_by_where(
            select_clause_value="organization_profile_id",
            where="organization_id = %s AND profile_id = %s",
            params=(organization_id, profile_id)
        )

        return organization_profile_id

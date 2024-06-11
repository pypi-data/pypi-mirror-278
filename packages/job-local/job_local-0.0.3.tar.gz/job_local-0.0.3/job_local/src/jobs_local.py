from database_mysql_local.generic_crud_ml import GenericCRUDML
from database_mysql_local.generic_mapping import GenericMapping
from group_local.groups_local import GroupsLocal
from group_remote.groups_remote import GroupsRemote
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger

from .jobs_local_constants import JobsLocalConstants

logger = Logger.create_logger(object=JobsLocalConstants.JOBS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

DEFAULT_SCHEMA_NAME = "job_title"
DEFAULT_TABLE_NAME = "job_title_table"
DEFAULT_ML_TABLE_NAME = "job_title_ml_table"
DEFAULT_ML_VIEW_NAME = "job_title_ml_en_view"
DEFAULT_VIEW_TABLE_NAME = "job_title_view"
DEFAULT_ID_COLUMN_NAME = "job_title_id"
DEFAULT_ML_ID_COLUMN_NAME = "job_title_ml_id"
DEFAULT_VIEW_WITH_DELETED_AND_TEST_DATA = "job_title_with_deleted_and_test_data_view"


class JobsLocal(GenericCRUDML):

    def __init__(self, is_test_data: bool = False):
        GenericCRUDML.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                               default_table_name=DEFAULT_TABLE_NAME,
                               default_ml_table_name=DEFAULT_ML_TABLE_NAME,
                               default_ml_view_table_name=DEFAULT_ML_TABLE_NAME,
                               default_view_with_deleted_and_test_data=DEFAULT_VIEW_WITH_DELETED_AND_TEST_DATA,
                               default_id_column_name=DEFAULT_ID_COLUMN_NAME,
                               is_test_data=is_test_data)
        self.groups_local = GroupsLocal(is_test_data=is_test_data)
        self.groups_remote = GroupsRemote(is_test_data=is_test_data)

    # TODO: we use this method?
    def process_job_title(self, contact_id: int, job_title: str) -> list[tuple[int, str]]:
        """
        Process the job title for a contact by checking if related groups exist and linking them.

        Args:
        - contact_id (int): The ID of the contact.
        - job_title (str): The job title associated with the contact.

        Returns:
        - List[Tuple[int, str]]: A list of tuples containing linked group IDs and titles.
        """
        if job_title is None:
            return []
        # Creating an instance of GenericMapping
        generec_mapping = GenericMapping(
            default_entity_name1='contact', default_entity_name2='group', default_schema_name='contact_group')

        # Retrieving all group names
        groups_names = self.groups_local.get_all_groups_names()  # TODO: cache in group_local

        # Initializing lists to store groups to link and groups that are successfully linked
        # Iterating through group names to find matching groups based on job_title
        groups_to_link = [group for group in groups_names if group and job_title in group]
        groups_linked = []

        # If no matching groups found based on job_title
        if not groups_to_link:
            # Creating a new group with the job_title
            lang_code = LangCode.detect_lang_code_restricted(text=job_title, default_lang_code=LangCode.ENGLISH)
            # TODO Why do we need the 1st parameter? [why not?]
            group_id = self.groups_remote.create_group(
                lang_code=lang_code, is_interest=True, title=job_title)
            # Inserting mapping between contact and the newly created group
            generec_mapping.insert_mapping(entity_name1='contact', entity_name2='group',
                                           entity_id1=contact_id, entity_id2=group_id)
            groups_linked.append((group_id, job_title))
        else:
            # Linking contact with existing groups found based on job_title
            for group in groups_to_link:
                group_id = GroupsRemote().get_group_by_group_name(
                    group_name=group).json()['data'][0]['id']
                generec_mapping.insert_mapping(entity_name1='contact', entity_name2='group',
                                               entity_id1=contact_id, entity_id2=group_id)
                groups_linked.append((group_id, group))

        # Logging the success of processing job title and returning linked group IDs and titles

        # TODO Please add a suffix to all relevant variables i.e. groups_linked
        return groups_linked

    def insert_job_title(self, *, job_title_dict: dict) -> tuple[int,int]:
        """
        Insert a job title into the database.

        Args:
        - job_title_dict (dict): The dictionary containing the job title information.

        Returns:
        - int or None: The ID of the inserted job title if successful, else None.
        """
        logger.start("start insert job_title", object=job_title_dict)
        title = job_title_dict.get("title")
        lang_code = LangCode.detect_lang_code_restricted(text=title, default_lang_code=LangCode.ENGLISH)
        job_title_data_dict : dict = {
            "name": title,
        }
        job_title_ml_data_dict: dict = {
            "title": title,
            "lang_code": lang_code,
            "is_title_approved": job_title_dict.get("is_title_approved")
        }
        # TODO: make it a transaction
        job_title_id = super().insert(data_dict=job_title_data_dict, ignore_duplicate=True)
        job_title_ml_id = super().insert(data_dict=job_title_ml_data_dict, ignore_duplicate=True)
        logger.end("end insert job_title", object={"job_title_id": job_title_id})
        return job_title_id, job_title_ml_id

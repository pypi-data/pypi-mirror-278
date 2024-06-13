from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger

from .jobs_local_constants import JobsLocalConstants

logger = Logger.create_logger(object=JobsLocalConstants.JOBS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

DEFAULT_SCHEMA_NAME = "job_title"
DEFAULT_TABLE_NAME = "job_title_table"
DEFAULT_ML_TABLE_NAME = "job_title_ml_table"
DEFAULT_ML_VIEW_NAME = "job_title_ml_en_view"
DEFAULT_VIEW_TABLE_NAME = "job_title_view"
DEFAULT_COLUMN_NAME = "job_title_id"
DEFAULT_ML_ID_COLUMN_NAME = "job_title_ml_id"
DEFAULT_VIEW_WITH_DELETED_AND_TEST_DATA = "job_title_with_deleted_and_test_data_view"


class JobsLocal(GenericCRUDML):

    def __init__(self, is_test_data: bool = False):
        GenericCRUDML.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                               default_table_name=DEFAULT_TABLE_NAME,
                               default_ml_table_name=DEFAULT_ML_TABLE_NAME,
                               default_ml_view_table_name=DEFAULT_ML_TABLE_NAME,
                               default_view_with_deleted_and_test_data=DEFAULT_VIEW_WITH_DELETED_AND_TEST_DATA,
                               default_column_name=DEFAULT_COLUMN_NAME,
                               is_test_data=is_test_data)

    def insert_job_title(self, *, job_title_dict: dict) -> tuple[int, int]:
        """
        Insert a job title into the database.

        Args:
        - job_title_dict (dict): The dictionary containing the job title information.

        Returns:
        - int or None: The ID of the inserted job title if successful, else None.
        """
        logger.start("start insert job_title", object=job_title_dict)
        title = job_title_dict.get("title")
        name = job_title_dict.get("name")
        lang_code = LangCode.detect_lang_code_restricted(text=title, default_lang_code=LangCode.ENGLISH)
        job_title_data_dict: dict = {
            "name": name,
        }
        # TODO: make it a transaction
        select_result = super().select_one_tuple_by_column_and_value(
            view_table_name="job_title_ml_en_view", column_name="job_name",
            column_value=name, select_clause_value="job_title_id, job_title_ml_id")
        if select_result:
            job_title_id, job_title_ml_id = select_result
            logger.end("end insert job_title", object={"job_title_id": job_title_id})
            return job_title_id, job_title_ml_id
        else:
            job_title_id = super().insert(
                table_name=self.default_table_name,
                data_dict=job_title_data_dict, ignore_duplicate=True)
            job_title_ml_data_dict: dict = {
                "title": title,
                "lang_code": lang_code.value,
                "is_title_approved": job_title_dict.get("is_title_approved"),
                "job_title_id": job_title_id
            }
            job_title_ml_id = super().insert(
                table_name=self.default_ml_table_name,
                data_dict=job_title_ml_data_dict, ignore_duplicate=True)
            logger.end("end insert job_title", object={"job_title_id": job_title_id})
            return job_title_id, job_title_ml_id

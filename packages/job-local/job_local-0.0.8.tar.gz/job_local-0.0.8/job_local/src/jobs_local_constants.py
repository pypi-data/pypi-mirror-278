from logger_local.LoggerComponentEnum import LoggerComponentEnum


class JobsLocalConstants:
    JOBS_LOCAL_PYTHON_COMPONENT_ID = 290
    JOBS_LOCAL_PYTHON_COMPONENT_NAME = "job-local-python-package"
    DEVELOPER_EMAIL = "tal.g@circ.zone"
    JOBS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT = {
        'component_id': JOBS_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': JOBS_LOCAL_PYTHON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }

    JOBS_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
        'component_id': JOBS_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': JOBS_LOCAL_PYTHON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': DEVELOPER_EMAIL
    }

from logger_local.LoggerComponentEnum import LoggerComponentEnum

ORGANIZATION_PROFILE_LOCAL_PYTHON_COMPONENT_ID = 287
ORGANIZATION_PROFILE_LOCAL_PYTHON_COMPONENT_NAME = "organization-profile-local-python-package"
DEVELOPER_EMAIL = "tal.g@circ.zone"
ORGANIZATION_PROFILE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT = {
    'component_id': ORGANIZATION_PROFILE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': ORGANIZATION_PROFILE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

ORGANIZATION_PROFILE_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
    'component_id': ORGANIZATION_PROFILE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': ORGANIZATION_PROFILE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': DEVELOPER_EMAIL
}

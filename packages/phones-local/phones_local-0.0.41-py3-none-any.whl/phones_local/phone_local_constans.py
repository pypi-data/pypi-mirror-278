from logger_local.LoggerComponentEnum import LoggerComponentEnum

PHONE_LOCAL_PYTHON_COMPONENT_ID = 200
PHONE_LOCAL_PYTHON_COMPONENT_NAME = "phones_local_python_package/src/phones_local.py"
DEVELOPER_EMAIL = 'jenya.b@circ.zone'

code_object_init = {
    'component_id': PHONE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': PHONE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": DEVELOPER_EMAIL
}

test_object_init = {
    'component_id': PHONE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': PHONE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    "developer_email": DEVELOPER_EMAIL
}

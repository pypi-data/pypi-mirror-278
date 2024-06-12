from logger_local.LoggerComponentEnum import LoggerComponentEnum


class GoogleContactConstants:
    class LoggerSetupConstants:
        GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 188
        GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'google-contact-local-python-package/google-contacts.py'
        OLD_DEVELOPER_EMAIL = 'valeria.e@circ.zone'
        DEVELOPER_EMAIL = 'tal.g@circ.zone'
        GOOGLE_CONTACT_LOCAL_CODE_LOGGER_OBJECT = {
            'component_id': GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
            'component_name': GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
            'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
            'developer_email': DEVELOPER_EMAIL
        }
        GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
            'component_id': GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
            'component_name': GOOGLE_CONTACT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
            'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
            'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
            'developer_email': DEVELOPER_EMAIL
        }

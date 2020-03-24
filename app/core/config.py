import os
import urllib


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ('TRUE', '1')
    return result


API_V1_STR = '/api/v1'

SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

SERVER_NAME = os.getenv('SERVER_NAME')
SERVER_HOST = os.getenv('SERVER_HOST')
BACKEND_CORS_ORIGINS = os.getenv(
    'BACKEND_CORS_ORIGINS',
    'http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080',
)
PROJECT_NAME = os.getenv('PROJECT_NAME', 'EECI_API')
SENTRY_DSN = os.getenv("SENTRY_DSN")

MSSQL_SERVER = os.getenv('MSQL_SERVER', '10.214.65.65,1433')
MSSQL_USER = os.getenv('MSSQL_USER', 'sa')
MSQL_PASSWORD = os.getenv('MSSQL_PASSWORD', 'EECI_sa_!2019-05-24')
MSSQL_DB = os.getenv('MSSQL_DB', 'EECI_DB')
MSSQL_PARAMS = urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={MSSQL_SERVER};'
                                 f'DATABASE={MSSQL_DB};UID={MSSQL_USER};PWD={MSQL_PASSWORD}')
SQLALCHEMY_DATABASE_URI = (
    'mssql+pyodbc:///?odbc_connect=%s' % MSSQL_PARAMS
)

FIRST_SUPERUSER = os.getenv('FIRST_SUPERUSER', 'fastAdmin')
FIRST_SUPERUSER_PASSWORD = os.getenv('FIRST_SUPERUSER_PASSWORD', 'asd')

USERS_OPEN_REGISTRATION = getenv_boolean('USERS_OPEN_REGISTRATION', True)

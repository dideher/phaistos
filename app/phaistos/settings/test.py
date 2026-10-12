import os
from phaistos.settings.development import *

# Settings used by the test suite (CI). The database backend is selected with DB_ENGINE:
#   sqlite (default)  -> the development sqlite database
#   mysql | mariadb   -> a MySQL/MariaDB server, configured like production

DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite')

if DB_ENGINE in ('mysql', 'mariadb'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'phaistos_db'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASS', 'root'),
            'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET default_storage_engine=INNODB; SET sql_mode='STRICT_TRANS_TABLES'",
                'isolation_level': 'read committed',
            },
            'TEST': {
                'CHARSET': 'utf8mb4',
                'COLLATION': 'utf8mb4_unicode_ci',
            },
        }
    }
elif DB_ENGINE != 'sqlite':
    raise ValueError(f"Unsupported DB_ENGINE '{DB_ENGINE}', expected sqlite, mysql or mariadb")

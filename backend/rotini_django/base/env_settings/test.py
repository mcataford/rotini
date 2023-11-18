"""
Settings overrides for test environments.
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "test",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

USER_UPLOAD_ROOT = "/tmp"

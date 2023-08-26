# pylint: disable=unused-import, wildcard-import, unused-wildcard-import, too-few-public-methods
import os
import typing

IS_CI = os.getenv("ROTINI_CI")
IS_TEST = os.getenv("ROTINI_TEST")
IS_MIGRATE = os.getenv("ROTINI_MIGRATE")


class Settings:
    """
    Representation of the configuration settings available to the
    application.
    """

    ENV: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    STORAGE_ROOT: typing.Optional[str] = "."

    def __init__(self, *_, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def extract_settings(env: str, imported_module) -> Settings:
    """
    Extracts all the exposed values from the given module and
    creates a corresponding Settings object.
    """
    imported_values = {
        k: v for k, v in imported_module.__dict__.items() if not k.startswith("__")
    }
    return Settings(ENV=env, **imported_values)


if IS_CI is not None:
    import envs.ci as ci_config

    settings = extract_settings("ci", ci_config)
elif IS_TEST is not None:
    import envs.test as test_config

    settings = extract_settings("test", test_config)
elif IS_MIGRATE is not None:
    import envs.migrate as migrate_config

    settings = extract_settings("migrate", migrate_config)
else:
    import envs.local as local_config

    settings = extract_settings("local", local_config)

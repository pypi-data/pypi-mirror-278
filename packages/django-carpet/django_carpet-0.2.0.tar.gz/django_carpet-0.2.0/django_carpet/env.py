# Django
from django.conf import settings

# Foundation
from .choices import EnvChoices


def exec_mode() -> str:
    """Gets the `EXEC_MODE` variable from the settings, informing the current state of runtime

    Returns:
        A member of `EnvChoices`
    """
    return getattr(settings, "EXEC_MODE", EnvChoices.NORMAL)


def is_debug() -> bool:
    """
    Checks if the application is in DEBUG mode or not. This function does not differntiates
    between tests or a running server
    """
    return settings.DEBUG

def is_production() -> bool:
    """
    Checks if the application is in the production mode or not. For the application to be
    in production, the `DEBUG` mode must be `false` and the `exec_mode` must be `normal`
    """
    return is_debug() is False and exec_mode() == EnvChoices.NORMAL

def is_testing() -> bool:
    """
    Checks if the application is in a unit test or E2E test.
    """
    return exec_mode() in [EnvChoices.E2E, EnvChoices.TEST]
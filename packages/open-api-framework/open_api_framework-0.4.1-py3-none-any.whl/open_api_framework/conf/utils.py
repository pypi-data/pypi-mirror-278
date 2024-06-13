import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from decouple import Csv, config as _config, undefined
from sentry_sdk.integrations import DidNotEnable, django, redis


def config(option: str, default: Any = undefined, *args, **kwargs):
    """
    Pull a config parameter from the environment.

    Read the config variable ``option``. If it's optional, use the ``default`` value.
    Input is automatically cast to the correct type, where the type is derived from the
    default value if possible.

    Pass ``split=True`` to split the comma-separated input into a list.
    """
    if "split" in kwargs:
        kwargs.pop("split")
        kwargs["cast"] = Csv()
        if isinstance(default, list):
            default = ",".join(default)

    if default is not undefined and default is not None:
        kwargs.setdefault("cast", type(default))
    return _config(option, default=default, *args, **kwargs)


def get_sentry_integrations() -> list:
    """
    Determine which Sentry SDK integrations to enable.
    """
    default = [
        django.DjangoIntegration(),
        redis.RedisIntegration(),
    ]
    extra = []

    try:
        from sentry_sdk.integrations import celery
    except DidNotEnable:  # happens if the celery import fails by the integration
        pass
    else:
        extra.append(celery.CeleryIntegration())

    return [*default, *extra]


def strip_protocol_from_origin(origin: str) -> str:
    parsed = urlparse(origin)
    return parsed.netloc


def get_project_dirname() -> str:
    return config("DJANGO_SETTINGS_MODULE").split(".")[0]


def get_django_project_dir() -> str:
    # Get the path of the importing module
    base_dirname = get_project_dirname()
    return Path(sys.modules[base_dirname].__file__).parent

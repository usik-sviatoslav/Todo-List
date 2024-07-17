from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS += ["localhost", "127.0.0.1"]  # noqa: F405

INSTALLED_APPS += [  # noqa: F405
    "silk",
]

MIDDLEWARE += [  # noqa: F405
    "silk.middleware.SilkyMiddleware",
]

BASE_FRONTEND_URL = os.getenv("DEV_FRONTEND_URL")  # noqa: F405

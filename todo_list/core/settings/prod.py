from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS += eval(os.getenv("ALLOWED_PROD_HOSTS"))  # noqa: F405

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "django_file": {
            "level": "ERROR",
            "class": "logging.TimedRotatingFileHandler",
            "filename": "/var/log/todo-list/django_errors.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "formatter": "verbose",
        },
        "celery_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "/var/log/celery/celery_errors.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django": {"handlers": ["django_file"], "level": "ERROR", "propagate": True},
        "celery": {"handlers": ["celery_file"], "level": "ERROR", "propagate": True},
    },
}

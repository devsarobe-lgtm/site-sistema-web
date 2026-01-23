from django.conf import settings


def analytics(_request):
    return {
        "IS_PROD": not getattr(settings, "DEBUG", True),
    }

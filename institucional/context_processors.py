from django.conf import settings


def analytics(_request):
    return {
        "GTM_ID": getattr(settings, "GTM_ID", ""),
        "IS_PROD": not getattr(settings, "DEBUG", True),
    }

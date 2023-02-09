from django.conf import settings


def static_root(request):

    return {
        "STATIC_ROOT": settings.STATIC_ROOT
    }

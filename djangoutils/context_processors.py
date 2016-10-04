from django.conf import settings


def google_maps(context):
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}

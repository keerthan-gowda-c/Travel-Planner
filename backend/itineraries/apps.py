from django.apps import AppConfig


class ItinerariesConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = 'itineraries'

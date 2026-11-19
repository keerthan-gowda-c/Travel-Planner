from django.apps import AppConfig


class ExpenseConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = 'expenses'

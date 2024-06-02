from django.apps import AppConfig


class AppConfig(AppConfig):
    """Configuración de la aplicación."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

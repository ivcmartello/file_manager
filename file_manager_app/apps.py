"""File manager apps"""
from django.apps import AppConfig


class FileManagerAppConfig(AppConfig):
    """File manager app config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "file_manager_app"

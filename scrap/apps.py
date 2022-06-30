from tabnanny import verbose
from django.apps import AppConfig


class ScrapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrap'
    verbose_name = "Приложение по сбору вакансий"

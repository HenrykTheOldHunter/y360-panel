from django.apps import AppConfig
from django.db.utils import OperationalError
class Y360Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'y360'

    def ready(self):
        from .models import update
        try:
            update() #updating/creating db
        except OperationalError:
            print("База данных не была обновлена (не существует)")
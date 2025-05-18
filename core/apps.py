from django.apps import AppConfig

class CoreConfig(AppConfig):  # Optional: also rename the class
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'  # ✅ Match the new folder name
from django.apps import AppConfig
from django.db.models.signals import post_save

# from .models import Strategy
# from .signals import change_my_name_plz

class RuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rule'

    def ready(self):
        import rule.signals
        
        
# class RuleConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'rule'


 

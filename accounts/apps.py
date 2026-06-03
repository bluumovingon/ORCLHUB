from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    for group_name in ['Admin', 'Editor', 'User']:
        Group.objects.get_or_create(name=group_name)

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)


from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'accounts'
    label = 'accounts'
    verbose_name = 'Accounts'

    def ready(self):
        import accounts.signals

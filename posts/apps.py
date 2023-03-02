from django.apps import AppConfig


class PostsAppConfig(AppConfig):
    name = 'posts'
    label = 'posts'
    verbose_name = 'Posts'

    def ready(self):
        import posts.signals

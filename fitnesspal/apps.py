from django.apps import AppConfig


class FitnesspalConfig(AppConfig):
    name = 'fitnesspal'

    def ready(self):
        import fitnesspal.signals
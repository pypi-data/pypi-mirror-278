from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy
from .config import LANGUAGE_CODE, LANGUAGES, LANGUAGES_LOCAL, APP_TRANSLATION_PATH, APP_LOCALE_PATH, SYSTEM_TRANSLATION_TAGS

_LOCALE_PATHS = []
_LOCALE_PATHS.append(APP_LOCALE_PATH)

class DjangoInternationalizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_internationalization'
    verbose_name = gettext_lazy('Internationalization')

    def ready(self) -> None:

        self.LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', LANGUAGE_CODE)
        self.LANGUAGES = getattr(settings, 'LANGUAGES', LANGUAGES)
        self.LANGUAGES_LOCAL = getattr(settings, 'LANGUAGES_LOCAL', LANGUAGES_LOCAL)

        # This is the path where the excel translation files are stored
        self.TRANSLATION_PATH = getattr(settings, 'TRANSLATION_PATH', APP_TRANSLATION_PATH)

        # This is a list of paths where the .po and .mo translation files are stored
        self.LOCALE_PATHS = getattr(settings, 'LOCALE_PATHS', [])
        if self.LOCALE_PATHS == []:
            self.LOCALE_PATHS = _LOCALE_PATHS

        # This is a list of tags that are used to identify system translations
        self.SYSTEM_TRANSLATION_TAGS = getattr(settings, 'SYSTEM_TRANSLATION_TAGS', SYSTEM_TRANSLATION_TAGS)

        # [Used for testing purposes] This is a list of all attributes of the settings module
        self.all_attributes = dir(settings)

        return super().ready()


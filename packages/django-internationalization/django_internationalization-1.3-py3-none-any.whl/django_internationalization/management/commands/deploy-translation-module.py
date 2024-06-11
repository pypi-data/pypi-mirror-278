from sys import stdout
from django.core.management import call_command
from django.core.management.base import BaseCommand
from ...utilities import get_languages
from ...models import Language, TranslationTag
from django.apps import apps
import os





class Command(BaseCommand):

    help = '''This command prepares the translation module by creating the 
            necessary Language and TranslationTag instances.'''

    def handle(self, *args, **kwargs) -> None:

        call_command('makemigrations')
        call_command('migrate')

        language_codes = [key for key in get_languages().keys()]
        #raise Exception(language_codes)
        Language.create_bulk(language_codes)

        translation_tags = apps.get_app_config('django_internationalization').SYSTEM_TRANSLATION_TAGS
        TranslationTag.create_bulk(translation_tags)

        LOCALE_PATHS = apps.get_app_config('django_internationalization').LOCALE_PATHS

        for path in LOCALE_PATHS:
            if not os.path.exists(path):
                os.makedirs(path)

        self.compile(language_codes)

    def compile(self, language_codes) -> None:
        language_codes = [key.replace('-', '_') for key in get_languages().keys()]
        #try:
        for code in language_codes:
            call_command('makemessages', f'--locale={code}')

        call_command('compilemessages')
        
        #except:
        #    stdout.write('''You need to install GNU text tools v0.15 or newer for this command to work properly.
        #                    Please use the following link to install the necessary tools: https://www.gnu.org/software/gettext/''')


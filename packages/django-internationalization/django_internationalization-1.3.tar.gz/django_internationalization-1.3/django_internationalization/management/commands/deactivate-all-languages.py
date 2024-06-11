from sys import stdout
from django.core.management.base import BaseCommand
from ...models import Language


class Command(BaseCommand):
    help = '''This command deactivates all languages.'''

    def handle(self, *args, **options) -> None:
        stdout.write('Deactivating all languages...\n')
        Language.deactivate_all_languages()



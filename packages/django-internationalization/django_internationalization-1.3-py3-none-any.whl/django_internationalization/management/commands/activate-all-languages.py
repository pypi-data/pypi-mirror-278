from django.core.management.base import BaseCommand
from numpy import std
from ...models import Language
from django.core.management.base import CommandParser
from sys import stdout


class Command(BaseCommand):
    help = '''This command activates and sets all languages to live.'''

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--set-live',
            '-sl',
            required=False,
            action='store_true',
            default=False,
            help='Specifies whether to set the languages to live. Default is False.'
        )

    def handle(self, *args, **options) -> None:
        stdout.write('Activating all languages...\n')
        Language.activate_all_languages(set_live=options.get('set_live', False))



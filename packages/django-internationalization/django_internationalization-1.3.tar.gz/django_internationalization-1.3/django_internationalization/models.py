from __future__ import unicode_literals, absolute_import
from django.db import models
from django.utils.translation import gettext_lazy
from django.conf import settings
from django.apps import apps
import os
import shutil
import zipfile
from .utilities import get_languages, slugify, list_to_string, list_to_dict
from .config import LIST_OF_COUNTRIES, LANGUAGE_DATA
from typing import Union
from uuid import uuid4
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.core.management import call_command
import polib
import xlwt
import xlsxwriter
import pandas
from numpy import nan



class Language(models.Model):

    LIST_OF_COUNTRIES = LIST_OF_COUNTRIES
    LANGUAGE_DATA = LANGUAGE_DATA

    code = models.CharField(primary_key=True, unique=True, max_length=12, verbose_name=gettext_lazy('Language code'))
    name = models.CharField(unique=False, max_length=32, verbose_name=gettext_lazy('Language name'))

    active = models.BooleanField(default=False, verbose_name=gettext_lazy('Active'))
    live = models.BooleanField(default=False, verbose_name=gettext_lazy('Live'))

    country = models.CharField(max_length=20, choices=LIST_OF_COUNTRIES, verbose_name=gettext_lazy('Country'), null=True, blank=True)

    class Meta:
        verbose_name = gettext_lazy('Language')
        verbose_name_plural = gettext_lazy('Languages')

    class InvalidLanguageCode(Exception):

        def __init__(self, code):
            self.message = f"Invalid language: {code}. Please define this language inside the LANGUAGES tuple in your settings file and try again."
            super().__init__(self.message)  

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'
    
    def save(self, *args, **kwargs) -> None:

        languages = get_languages()

        if self.code in languages:
            #if languages[self.code] == self.name:
            if self.active is False and self.live is True:
                self.live = False

            return super().save(*args, **kwargs) 
            
        raise self.InvalidLanguageCode(self)
    
    def delete(self, *args, **kwargs) -> None:
        if self.code not in get_languages():
            return super().delete(*args, **kwargs)
        else:
            self.deactivate()

    def deactivate(self) -> None:
        self.active = False
        self.save()

    @classmethod
    def get_active_languages(cls, name_local=True) -> dict[str, str]:
        '''Returns a dictionary of active languages.'''
        languages = get_languages(name_local=name_local)
        return {language.code: languages[language.code] for language in cls.objects.filter(active=True)}
        #return {language.code: language.name for language in cls.objects.filter(active=True)}
    
    @classmethod
    def get_live_languages(cls, name_local=True) -> dict[str, str]:
        '''Returns a dictionary of live languages.'''
        languages = get_languages(name_local=name_local)
        return {language.code: languages[language.code] for language in cls.objects.filter(live=True)}
        #return {language.code: language.name for language in cls.objects.filter(live=True)}

    @classmethod
    def create_bulk(cls, languages: Union[list,tuple]) -> None:
        '''Creates multiple languages based of an list/tuple input.'''

        if isinstance(languages, (list, tuple)) is False:
            raise TypeError('The input should be a list or a tuple.')

        all_languages = get_languages()
        default_language = apps.get_app_config('django_internationalization').LANGUAGE_CODE

        for value in languages:
            if value in all_languages and not cls.objects.filter(code=value).exists():
                cls.objects.create(
                    code=value, 
                    name=cls.LANGUAGE_DATA[value]['name_local'] if cls.LANGUAGE_DATA[value] else all_languages[value],
                    active=True if value == default_language else False,
                    live=True if value == default_language else False,
                    country=cls.LANGUAGE_DATA[value]['country'] if cls.LANGUAGE_DATA[value]['country'] else None
                )

    @classmethod
    def activate_all_languages(cls, set_live:bool = True) -> None:
        '''Activates all languages.'''

        for language in cls.objects.all():
            language.active = True
            if set_live:
                language.live = True
            language.save()

    @classmethod
    def deactivate_all_languages(cls) -> None:
        '''Deactivates all languages.'''

        for language in cls.objects.all():
            language.deactivate()

class TranslationTag(models.Model):
    
    name = models.CharField(primary_key=True, unique=True, max_length=256, verbose_name=gettext_lazy('Tag'))

    class Meta:
        verbose_name = gettext_lazy('Translation tag')
        verbose_name_plural = gettext_lazy('Translation tags')

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.name = slugify(self.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        system_tags = apps.get_app_config('django_internationalization').SYSTEM_TRANSLATION_TAGS

        if not self.name in system_tags:
            super().delete(*args, **kwargs)

    @classmethod
    def create_bulk(cls, tags: Union[list,tuple]) -> None:
        '''Creates multiple tags based of an list/tuple input.'''

        if isinstance(tags, (list, tuple)) is False:
            raise TypeError('The input should be a list or a tuple.')
        
        for tag in tags:
            if not cls.objects.filter(name=tag).exists():
                cls.objects.create(name=tag)
 
class Translation(models.Model):

    key = models.CharField(max_length=128, editable=False, default=None, null=True, blank=True, verbose_name=gettext_lazy('Key'))

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='translations', null=True, blank=True, verbose_name=gettext_lazy('Language'))
    tags = models.ManyToManyField(TranslationTag, related_name='translations', blank=True, verbose_name=gettext_lazy('Tags'))

    content = models.TextField(null=True, blank=True, verbose_name=gettext_lazy('Content'))
    protected = models.BooleanField(default=False, editable=True if getattr(settings, 'DEBUG', True) else False, verbose_name=gettext_lazy('Protected'))

    # Constants
    valid_extensions = ['xls', 'xlsx']

    class Meta:
        verbose_name = gettext_lazy('Translation')
        verbose_name_plural = gettext_lazy('Translations')

    class InvalidLanguageError(Exception):

        def __init__(self, code):
            self.message = f"Invalid language code: {code}. Please create a Language object with that specific code before you proceed."
            super().__init__(self.message)

    class InvalidExtensionError(Exception):

        def __init__(self, extension):
            self.message = f"Invalid file extension: {extension}. The extension should be either .xls or .xlsx."
            super().__init__(self.message)

    class InactiveLanguageError(Exception):
            
            def __init__(self, code):
                languages = get_languages()

                self.message = f"The language with code {languages[code]} ({code}) is not active. Please activate it before you proceed."
                super().__init__(self.message)

    class InvalidUploadError(Exception):

        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    def __init__(self, *args, **kwargs) -> None:

        if 'valid_extensions' in kwargs:
            del kwargs['valid_extensions']

        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.key} ({self.language})'
    
    def save(self, sync_copies:bool = True, *args, **kwargs) -> None:

        # Generate a key if it does not exist
        if self.key == None:
            while True:
                key = uuid4().hex
                if not Translation.objects.filter(key=key).exists():
                    self.key = key
                    break

        super().save(*args, **kwargs)
        
        # Create or synchronize copies of the translation instance
        if sync_copies:
            self.__create_and_sync_copies__()

    def delete(self, *args, **kwargs) -> None:
        if not self.protected:
            super().delete(*args, **kwargs)

    @classmethod
    def create(cls, code:str, content:str, tags:Union[list,tuple] = [], key:str = None, protected:bool = False) -> 'Translation':
        '''Creates a new translation object.'''

        languages = Language.get_active_languages()
        if code not in languages:
            raise cls.InvalidLanguageError(code)
        
        for tag in tags:
            TranslationTag.objects.get_or_create(name=tag)

        key = key if key else uuid4().hex
        tags_objects = TranslationTag.objects.filter(name__in=tags)

        translation = cls.objects.create(
            key=key,
            language=Language.objects.get(code=code),
            content=content,
            protected=protected
        )
        translation.tags.set(tags_objects)

    def __create_and_sync_copies__(self, sync_content:bool = False) -> None:
        '''Creates or synchronizes copies of the translation instance.'''
        
        languages = Language.get_active_languages()
        for code in languages:
            language = Language.objects.get(code=code)
            tags = self.tags.all()

            if not Translation.objects.filter(key=self.key, language__code=code).exists():
                translation = Translation.objects.create(
                    key=self.key,
                    language=language,
                    content=self.content,
                    protected=self.protected
                )
                translation.tags.set(self.tags.all())
            else:
                translation = Translation.objects.get(key=self.key, language__code=code)
                translation.protected = self.protected
                translation.content = self.content if sync_content else translation.content
                translation.tags.set(tags)
                translation.save(sync_copies=False)

    @classmethod
    def generate_translation_file(cls, from_language:str, to_languages:Union[str, list[str]], extension:str, get_system_translations:bool = False) -> 'HttpResponse':

        languages = get_languages()
        valid_extensions = cls.valid_extensions

        if type(to_languages) is str:
            to_languages = [to_languages]

        if from_language is None:
            from_language = apps.get_app_config('django_internationalization').LANGUAGE_CODE

        # Check if the from and to languages are valid for the project
        if from_language not in languages:
            raise cls.InvalidLanguageError(from_language)
        if not Language.objects.filter(code=from_language).exists():
            raise cls.InactiveLanguageError(from_language)
        
        for l in to_languages:
            if l not in languages or not Language.objects.filter(code=l).exists():
                raise cls.InvalidLanguageError(l)
            else:
                if Language.objects.get(code=l).active is False:
                    raise cls.InactiveLanguageError(l)

        # Check if the extension is valid
        if extension not in valid_extensions:
            raise cls.InvalidExtensionError()
        
        # Generate the translation file based on extension type
        # (Formats could be expanded in the future)
        if extension in ['xls', 'xlsx']:
            return cls.create_workbook(from_language, to_languages, extension, get_system_translations)
        
    @classmethod
    def create_workbook(cls, from_language:str, to_languages:list[str], extension:str, get_system_translations:bool = False) -> 'HttpResponse':
        '''Creates workbooks for specified language.'''

        files_to_zip = []
        dict_of_languages = get_languages()
        system_tag_objects = TranslationTag.objects.filter(name__in=apps.get_app_config('django_internationalization').SYSTEM_TRANSLATION_TAGS)


        # Create a temporary directory for the files
        translation_path = apps.get_app_config('django_internationalization').TRANSLATION_PATH
        if not os.path.exists(translation_path):
            os.mkdir(translation_path)
        if not os.path.exists(f"{translation_path}/downloads"):
            os.mkdir(f"{translation_path}/downloads")
        temp_path = f"{translation_path}/downloads/{uuid4().hex}"
        os.mkdir(temp_path)

        # Get the translation objects
        if get_system_translations:
            translation_objects = Translation.objects.filter(language__code=from_language)
        else:
            translation_objects = Translation.objects.filter(language__code=from_language).exclude(tags__in=system_tag_objects)

        # Create the workbook for the from language
        for l in to_languages:

            translations = []

            # Translation objects
            for translation in translation_objects:
                translated_content = Translation.objects.get(key=translation.key, language__code=l).content
                translations.append((translation.key, translation.content, translated_content))

            # PO files
            if get_system_translations:
                po_file = polib.pofile(f"{apps.get_app_config('django_internationalization').LOCALE_PATHS[0]}/{l.replace('-', '_')}/LC_MESSAGES/django.po")
                for entry in po_file:
                    translations.append((entry.msgid, entry.msgid, entry.msgstr))

            # Create workbook path and Remove prior workbook if it exists
            file_path = f"{temp_path}/translation_{l}.{extension}"
            if os.path.isfile(file_path):
                os.remove(file_path)

            if extension == 'xls':
                # Sheet styles
                header_style = xlwt.easyxf('font: bold on; align: horiz center; align: vert center; font: bold on, height 280;')
                text_style_locked = xlwt.easyxf('align: vert center; align: wrap on;')
                text_style_unlocked = xlwt.easyxf('align: vert center; align: wrap on;')

                # Create workbook and sheet
                workbook = xlwt.Workbook(encoding='utf-8')
                sheet = workbook.add_sheet('Translations', cell_overwrite_ok=True)

                sheet.write(0, 0, 'ID', header_style)
                sheet.write(0, 1, dict_of_languages[from_language], header_style)
                sheet.write(0, 2, dict_of_languages[l], header_style)

                row = sheet.row(0)
                row.height = 1200
                row.height_mismatch = True

                sheet.col(0).hidden = 1
                sheet.col(1).width = 256 * 60
                sheet.col(2).width = 256 * 60

                # Write translations
                for i, item in enumerate(translations, 1):
                    sheet.write(i, 0, item[0], text_style_locked)
                    sheet.write(i, 1, item[1], text_style_locked)
                    sheet.write(i, 2, item[2], text_style_unlocked)

                workbook.save(file_path)
            elif extension == 'xlsx':
                # Create workbook and sheet
                workbook = xlsxwriter.Workbook(file_path)
                sheet = workbook.add_worksheet('Translations')

                # Styles
                header_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 20, 'text_wrap': True})
                hidden_header_format = workbook.add_format({'hidden': 1})
                text_format_locked = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True})
                text_format_unlocked = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'locked': False})

                # Set first row
                sheet.write(0, 0, 'ID', hidden_header_format)
                sheet.write(0, 1, dict_of_languages[from_language], header_format)
                sheet.write(0, 2, dict_of_languages[l], header_format)
                sheet.set_column(0, 0, 20)
                sheet.set_column(1, 2, 40)

                # Write translations
                for i, item in enumerate(translations, 1):
                    sheet.write(i, 0, item[0], text_format_locked)
                    sheet.write(i, 1, item[1], text_format_locked)
                    sheet.write(i, 2, item[2], text_format_unlocked)

                sheet.set_column(0, 0, None, None, {'hidden': True})

                sheet.protect()
                workbook.close()

            files_to_zip.append(file_path)

        # Zip the files
        try:
            zip_file_path = f"{temp_path}/translations.zip"
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                for file in files_to_zip:
                    file_name = os.path.basename(file)
                    arcname = file_name
                    zip_file.write(os.path.join(temp_path, file_name), arcname=arcname)

            with open(zip_file_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename=translations.zip'
                return response
        finally:
            shutil.rmtree(temp_path)

    @classmethod
    def upload_translation_file(cls, file_path:str) -> None:
        '''Uploads a translation file and updates the database and po/mo files.'''

        languages = get_languages()
        valid_extensions = cls.valid_extensions

        try:
            file_name = os.path.basename(file_path)
            extension = file_name.split('.')[-1]
            lang = file_name.split('.')[0].split('_')[-1]
        except:
            raise cls.InvalidUploadError('Something went wrong while processing the file. Please try again.')
 
        if extension not in valid_extensions:
            raise cls.InvalidExtensionError(f'The file must be one of the following extensions: {list_to_string(valid_extensions)}')
        
        if file_name.split('.')[0].split('_')[0] != 'translation':
            raise cls.InvalidUploadError('Please select the valid translations file.')

        if lang not in languages:
            raise cls.InvalidUploadError('Please select a valid translation file with a valid language code.')
        
        try:
            workbook = pandas.read_excel(file_path, index_col=None, usecols='A,C')
            workbook = workbook.replace(nan, '', regex=True)

            other_translations = []

            for item in workbook.values:
                key = item[0]
                content = item[1]

                if cls.objects.filter(key=key, language__code=lang).exists():
                    translation = cls.objects.get(key=key, language__code=lang)
                    translation.content = content
                    translation.save()
                else:
                    other_translations.extend([key, content])

            other_translations = list_to_dict(other_translations)

            po_file = polib.pofile(f"{apps.get_app_config('django_internationalization').LOCALE_PATHS[0]}/{lang.replace('-', '_')}/LC_MESSAGES/django.po")

            for entry in po_file:
                if entry.msgid in other_translations:
                    entry.msgstr = other_translations[entry.msgid]
            
            po_file.save()

            call_command('compilemessages')
        except:
            raise cls.InvalidUploadError('Something went wrong while processing the file. Please try again.')
        finally:
            if os.path.isfile(file_path):
                os.remove(file_path)
                
    

@receiver(post_save, sender=Language)
def language_activated(sender, instance, created, **kwargs):
    '''Automatically creates translation objects when a language is activated
    and calls the makemessages and compilemessages commands.'''

    if created:
        code = instance.code.replace("-", "_")
        call_command('makemessages', f'--locale={code}')
        call_command('compilemessages', f'--locale={code}')

    if instance.active:
        distinct_keys = Translation.objects.values('key').distinct()
        translations = Translation.objects.filter(key__in=[item['key'] for item in distinct_keys])
        for translation in translations:
            translation.__create_and_sync_copies__(sync_content=True)



class TranslationFile(models.Model):

    file = models.FileField(upload_to=f"{apps.get_app_config('django_internationalization').name}/translations/uploads", verbose_name=gettext_lazy('Translation file'))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('Uploaded at'))

    class Meta:
        verbose_name = gettext_lazy('Translation file')
        verbose_name_plural = gettext_lazy('Translation files')

    def __str__(self) -> str:
        return self.file.name
    


    
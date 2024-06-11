from django import forms
from django.utils.translation import gettext
from .models import Language, TranslationFile
from .utilities import get_languages
from django.apps import apps
from django.utils import translation


class LanguageSelector(forms.ModelForm):

    id = 'language-selector'

    # Behavior of the form
    open_on_hover = True
    open_on_click = True

    # Sets the class of the form. The default is 'default'
    style = 'default' 

    class Meta:
        model = Language
        fields = []

    class CustomModelChoiceField(forms.ModelChoiceField):

        def label_from_instance(self, obj) -> str:
            languages = get_languages()
            try:
                return languages[obj.code]
            except:
                return obj.name
            
    class CustomRadioSelect(forms.RadioSelect):

        flag_paths = []
        active_lang_name = None
        active_lang_code = None

        def __init__(self, *args, **kwargs):
            self.flag_paths.clear()
            super().__init__(*args, **kwargs)


        def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
            option_dict = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

            if value is not None:
                instance = self.choices.queryset.get(pk=value)

                # Add the flag path for the static string call in the template
                # You can change this value if you want to use a different path for your flags
                flag = f"{apps.get_app_config('django_internationalization').name}/flags/{instance.country}.svg" if instance.country else f"{apps.get_app_config('django_internationalization').name}/flags/NO-FLAG.svg"
                #if not flag in self.flag_paths:
                self.flag_paths.append(flag)

                # You can put any attribute you want here and they will appear in the input tag
                option_dict['attrs']['id'] = f'language-selector-code-{instance.code}'
                option_dict['attrs']['class'] = f"language-selector-item {'active' if instance.code == translation.get_language() else ''}"

                if instance.code == translation.get_language():
                    self.active_lang_name = instance.name
                    self.active_lang_code = instance.code


            return option_dict
        
    def __init__(self, *args, **kwargs):
        self.active_languages = Language.get_live_languages()
        super().__init__(*args, **kwargs)

    def _get_language_(self):
        '''Returns the current language code.'''
        
        l = translation.get_language()
        if '-' in l:
            return f"{l.split('-')[0]}-{l.split('-')[1].upper()}"
        else:
            return l

    def display(self) -> bool:
        return Language.get_live_languages().__len__() > 1
    
    def get_active_language(self) -> str:
        return self._get_language_()
    
    def get_active_language_flag(self) -> str:
        try:
            return Language.LANGUAGE_DATA[self._get_language_()]['country']
        except KeyError:
            return 'NO-FLAG'
    
    def get_active_language_name(self) -> str:
        return Language.objects.get(code=self._get_language_()).name

    
    language = CustomModelChoiceField(
        queryset = Language.objects.filter(live=True),
        widget = CustomRadioSelect(
            attrs = {
                'onchange': 'this.form.submit()',
                #'onclick': 'this.form.submit()',
                #'role': 'button',
                'tabindex': '-1'
            },
        ),
    )

class TranslationFilesUploadForm(forms.ModelForm):

    form_text = gettext('''
                    <p class="instruction">Click here or drag file to upload</p>
                    <p class="limitations">Only xls and xlsx files</p>
                   ''')
    
    no_file_text = gettext('- No file selected -')
    
    submit_text = gettext('Upload translation')

    upload_svg_path = f"{apps.get_app_config('django_internationalization').name}/upload.svg"
    close_svg_path = f"{apps.get_app_config('django_internationalization').name}/close-circle.svg"

    class Meta:
        model = TranslationFile
        fields = []

    translation_file = forms.FileField(
        widget = forms.FileInput(
            attrs = {
                'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
                'id': 'translation_file',
                'class': 'translation-upload-input',
                'tabindex': '-1'
            },
        ),
        label = None,
        required = False,
    )

class TranslationFilesDownloadForm(forms.ModelForm):

    submit_text = gettext('Download translation files')
    dropdown_placeholder = gettext('Select language')
    form_header = gettext('Download translation files')

    active_languages = []

    class Meta:
        model = Language
        fields = []

    class CustomModelChoiceField(forms.ModelChoiceField):

        def label_from_instance(self, obj) -> str:
            languages = get_languages(name_local=True)
            try:
                return languages[obj.code]
            except:
                return obj.name

    class CustomRadioSelect(forms.RadioSelect):

        def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
            option_dict = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

            if value is not None:
                instance = self.choices.queryset.get(pk=value)

                # You can put any attribute you want here and they will appear in the input tag
                option_dict['attrs']['id'] = f'language-selector-code-{instance.code}'
                option_dict['attrs']['class'] = f"language-selector-item {'active' if instance.code == translation.get_language() else ''}"




            return option_dict
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_languages = Language.get_active_languages(name_local=False)

    from_language = forms.ChoiceField(
        choices = active_languages,
        required=True
    )
    
    to_languages = forms.MultipleChoiceField(
        choices = active_languages,
        required=True,
    )

    all_languages = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'toggle-switch',
                'tabindex': '-1'
            }
        ),
        label = None
    )
    all_languages.content_after = gettext('<p>Download all languages</p>')

    get_system_translations = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'toggle-switch',
                'tabindex': '-1'
            }
        ),
        label = None
    )
    get_system_translations.content_after = gettext('<p>Include system translations</p>')

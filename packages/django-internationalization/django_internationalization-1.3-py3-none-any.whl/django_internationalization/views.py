from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django_internationalization.forms import LanguageSelector, TranslationFilesDownloadForm, TranslationFilesUploadForm
from django_internationalization.models import Language, Translation, TranslationFile
from django_internationalization.utilities import set_language
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy
from django.views import View

    
class Test(View):

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = {}

        context['language_selector'] = LanguageSelector()
        context['translation_files_download_form'] = TranslationFilesDownloadForm()
        context['translation_files_upload_form'] = TranslationFilesUploadForm()
        context['test'] = request.session.get('language', 'kurec')

        return render(request, 'base.html', context)
        
    def post(self, request, *args, **kwargs) -> HttpResponse:
        context = {}

        context['language_selector'] = LanguageSelector(request.POST)
        context['translation_files_download_form'] = TranslationFilesDownloadForm()
        context['translation_files_upload_form'] = TranslationFilesUploadForm()
        context['test'] = request.POST

        return render(request, 'base.html', context)

class ChangeLanguage(View):

    def post(self, request, *args, **kwargs) -> HttpResponse:
        set_language(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class DownloadTranslation(View):

    def post(self, request, *args, **kwargs) -> HttpResponse:


        # from_language = request.POST.get('from_language', request.session['language'] if 'language' in request.session else apps.get_app_config('django_internationalization').LANGUAGE_CODE)
        from_language = request.POST.get('from_language', None)
        if request.POST.get('all_languages', None):
            to_languages = Language.get_active_languages()
        else:
            to_languages = request.POST.getlist('to_languages')

        if not from_language or not to_languages:
            messages.error(request, gettext_lazy('Please select a source language and at least one target language to download the translation files for.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        return Translation.generate_translation_file(
            from_language = from_language,
            to_languages = to_languages,
            extension = 'xlsx',
            get_system_translations = request.POST.get('get_system_translations', False)
        )

class UploadTranslation(View):

    def post(self, request, *args, **kwargs) -> HttpResponse:

        try:
            if request.FILES.get('translation_file', None):
                file = TranslationFile.objects.create(file=request.FILES['translation_file'])
                Translation.upload_translation_file(file.file.path)
                file.delete()
                messages.success(request, gettext_lazy('The translation file has been uploaded successfully.'))
            else:
                messages.error(request, gettext_lazy('Please select a translation file to upload'))
        except:
            messages.error(request, gettext_lazy('The translation file was not uploaded.'))


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
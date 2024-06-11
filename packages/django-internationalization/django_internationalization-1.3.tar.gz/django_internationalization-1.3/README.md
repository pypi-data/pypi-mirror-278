# django-internationalization

## Description
A Django app used for translation and localization

## Features
- Mixed translation system using both the gettext utility and database entries
- Easy to use translation file exporting and importing

## Technologies Used
- Python
- Django
- GNU gettext

## Installation

0. You need GNU text tools v0.15 or newer installed for the app to function successfully. You can find it [here](https://www.gnu.org/software/gettext/)

1. Create your Django project and set up your virtual environment.
[Install virtualenv](https://virtualenv.pypa.io/en/stable/installation.html)
[User guide](https://virtualenv.pypa.io/en/stable/user_guide.html)

2. Install the app.
```
pip install django_internationalization
```

3. Add your app to the INSTALLED_APPS in your settings file.
```
    INSTALLED_APPS = [
        ...,
        'django_internationalization'
    ]
```

4. Add the locale middleware.
```
    MIDDLEWARE = [
        ...,
        'django.middleware.locale.LocaleMiddleware',
        ...,
    ]
```

5. Set your default LANGUAGE_CODE and LANGUAGES variables.
```
LANGUAGE_CODE = 'en-US'
LANGUAGES = (
    ("en-US", "English"),
    ("bg", "Bulgarian"),
    ...
)
```

You can also import the LANGUAGES or LANGUAGES_LOCAL variable and assign it in your settings. LANGUAGES contains the language names in English, while LANGUAGES_LOCAL contains the language names in their local scripts.
```
from django_internationalization.config import LANGUAGES_LOCAL

...

LANGUAGE_CODE = 'en-US'
LANGUAGES = LANGUAGES_LOCAL
```

6. Set your LOCALE_PATHS using the app's _LOCALE_PATHS variable
```
from django_internationalization.apps import _LOCALE_PATHS

...

LOCALE_PATHS = _LOCALE_PATHS
```

7. Include the app urls to your project's urls.
```
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_internationalization.urls'))
]
```

8. Put the following js and css files in the ```head``` tag of your main template:
```
<script src="https://code.jquery.com/jquery-3.7.1.slim.min.js"></script>

<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

<link rel="stylesheet" href="{% static 'django_internationalization/css/master.css' %}">
<script src="{% static 'django_internationalization/js/master.js' %}"></script>
```

9. In your console, go to your project folder and use the deploy-translation-module command
```
cd your_project_name
py manage.py deploy-translation-module
```

## Usage

### The Language model
The Language model has two important boolean values - **active** and **live**.

**active** shows if the language is activated for the project, but should not yet be seen by the end users. Existing translations are created for that language based on existing ones on activation. Deactivating a language does not delete already existing translations.

**live** should be used when the language is ready to be presented to the end users. It gets shown in the language selector.

The general workflow should be activating a language, creating or updating the translations for it and finally setting it live.

### Language Selector
The language selector is a form that displays the available **live** languages and switches the website language. 

#### Usage
To use it, you need to follow the steps below:
1. Pass the form in your view.
```
from django_internationalization.forms import LanguageSelector

class MyViwe(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['language_selector'] = LanguageSelector()
        return render(request, 'your_template.html', context)
```

2. Include the template inside your own template.
```
{% include 'ecom_django_translations/language-selector.html' with form=language_selector %}
```

* If you have less than two languages set to live, the form will not be displayed.

#### Form parameters
The form has a few parameters that can be changed.

**open_on_hover** (bool) and **open_on_click** (bool) can be toggled and are set to True by default. They dictate how the submenu is opened.

**style** sets the class of the form. This is used mainly for switching between different UI styles.

### Adding new languages to the project
To add a new language that does not exist, you need to append it to LANGUAGE_DATA inside the Language model.
You can do this by creating your ows Language model that inherits the original.

```
from django_internationalization.models import Language
from django.utils.translation import gettext_lazy

class MyLanguage(Language):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.LANGUAGE_DATA['your_language_code'] = {"name": gettext_lazy("Name in English"), "name_local": "Name in local script", "country": "CC"}
```

The **country** value should be one of the country codes in the **django_internationalization/config/LIST_OF_COUNTRIES** tuple

In your console, run makemessages and compilemessages:
```
py manage.py makemessages -l your_language_code
py manage.py compilemessages -l your_language_code
```

### Translations

#### Adding translations to your models
If you want to have different language versions of an entry for your model, you can set the specific field as a foreign key

```
from django.db import models
from django_internationalization.models import Translation

class MyModel(models.Model):

    content = models.ForeignKey('Translation', on_delete=models.CASCADE, related_name='translations', null=True, blank=True)
```

#### Downloading translation files
You can download translation files using TranslationFilesDownloadForm. It gathers both the Translation model entries and the contents of the gettext .po files.

1. Pass the form in your view.
```
from django_internationalization.forms import TranslationFilesDownloadForm

class MyViwe(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['translation_download_form'] = TranslationFilesDownloadForm()
        return render(request, 'your_template.html', context)
```

2. Include the template inside your own template.
```
{% include 'ecom_django_translations/translation-download.html' with form=translation_download_form %}
```

* The Translation model currently exports both **.xls**. and **..xlsx**. files, however currently only the latter is used.

* The "Include system translations" toggle controls if the gettext .po files should be included into the exported file.

#### Uploading a translation file
You can upload translation files (one by one) using TranslationFilesUploadForm. 

1. Pass the form in your view.
```
from django_internationalization.forms import TranslationFilesUploadForm

class MyViwe(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['translation_upload_form'] = TranslationFilesUploadForm()
        return render(request, 'your_template.html', context)
```

2. Include the template inside your own template.
```
{% include 'ecom_django_translations/translation-upload.html' with form=translation_upload_form %}
```

#### Showing translated conted in your templates
* You still need to manualy query for the translations in your database that use the Translation model. This can be done in a variety of ways, depending on your specific use case.

* If the Translation model content needs to display html, don't forget to add the 'safe' filter in the template that you're using.
```
{% your_html_translation|safe %}
```

#### Manually changing the website language
If you don't want to use the Language Selector, you can still change the website language by using the set_language utility function. The best use case here is including the function in the dispatch method of a View base class that's being used for all of your other views.
```
from django.views import View
from django_internationalization.utilities import set_language

class MyBaseView(View):
    def dispatch(self, request, *args, **kwargs):
        set_language(request, 'en-US')
        return super().dispatch(request, *args, **kwargs)

class SomePageView(MyBaseView):

    def get(self, *args, **kwargs):
        context = {}
        '''Do stuff'''
        return render(request, 'my_template.html', context)
```

### Other

#### Using the Django messages utility
Some of the forms have a set action pointing to a specific view, so we can't use form cleaning methods. This is why we've opted in for using django/contrib/messages for form errors. To see the messages, you need to:

1. Make sure you have 'django.contrib.messages' in your INSTALLED_APPS
```
INSTALLED_APPS = [
    ...
    'django.contrib.messages',
    ...
]
```

2. Put the following snippet in your main template
```
{% if messages %}
    <div class="messages">
        {% for message in messages %}
            <p class="{{message.tags}}">{{message}}</p>
        {% endfor %}
    </div>
{% endif %}
```

## License
[Mozilla Public License Version 2.0](LICENSE)


from typing import Union
from django.apps import apps
import re
from django.utils.translation import activate 
from .config import LANGUAGE_DATA, LANGUAGES, LANGUAGES_LOCAL


def list_to_dict(list: Union[list,tuple]) -> dict:
    '''
    Take a list or a tuple with an *even number* of objects and converts it 
    to a dictionary.
    '''

    if len(list) % 2 != 0:
        raise IndexError('Argument does not contain an even number of objects.')

    output = {}

    for i in range(0, len(list), 2):
        output[str(list[i])] = list[i+1]

    return output

def flatten_list(list: list) -> list:
    '''Flattens a list of lists.'''
    return [item for sublist in list for item in sublist]

def slugify(input:str) -> str:
    '''Slugifies input and returns an URL friendly string.'''
    
    input = re.sub(r'[^a-zA-Z0-9_-]', '-', str(input))
    input = input.replace(' ', '_').replace('\n', '_').replace('\t', '_').lower()

    return input

def list_to_string(list: Union[list,tuple]) -> str:
    '''Converts a list to a string.'''
    
    return str(list).replace('[', '').replace(']', '').replace('\'', '')

def get_languages(name_local=True) -> dict:
    '''
    Returns a dictionary of languages from the settings file.
    Format of dictionary: {'locale': 'name'}
    '''
    if name_local is True:
        return list_to_dict(flatten_list(apps.get_app_config('django_internationalization').LANGUAGES_LOCAL))
    else:
        return list_to_dict(flatten_list(apps.get_app_config('django_internationalization').LANGUAGES))
        
def set_language(request, language:str|None = None) -> None:
    '''Activates a language for translation.'''

    default_language = apps.get_app_config('django_internationalization').LANGUAGE_CODE
    all_languages = get_languages()

    l = language if language is not None else request.POST.get('language', request.session.get('language', default_language))
    l = l if l in all_languages else default_language

    l.replace('_', '-')

    activate(l)

    if request.session.get('language', None) != l:
        request.session['language'] = l
        request.session.save()
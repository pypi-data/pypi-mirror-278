from django.contrib import admin
from .models import Language, TranslationTag, Translation, TranslationFile
from django.conf import settings



class LanguageAdmin(admin.ModelAdmin):

    list_display = ('active', 'live', 'name', 'code', 'country')
    search_fields = ('active', 'live', 'name', 'code', 'country')

    readonly_fields = () if getattr(settings, 'DEBUG', True) else ('name', 'code')

    filter_horizontal = ()
    list_filter = ()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-live', '-active')

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        
        return actions

admin.site.register(Language, LanguageAdmin)


class TranslationTagAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ('name',)

    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    
admin.site.register(TranslationTag, TranslationTagAdmin)


class TranslationAdmin(admin.ModelAdmin):

    list_display = ('key', 'language', 'protected')
    search_fields = ('language__name',)

    readonly_fields = () if getattr(settings, 'DEBUG', True) else ('key', 'language', 'protected')

    filter_horizontal = ()
    list_filter = ()

    def save_model(self, request, obj, form, change) -> None:

        if not change:
            return super().save_model(request, obj, form, change)
        else:
            try:
                return super().save_model(request, obj, form, change)
            finally:
                instance = Translation.objects.get(pk=obj.pk)
                instance.tags.set(form.cleaned_data['tags'])
                instance.save()

admin.site.register(Translation, TranslationAdmin)

'''
class TranslationFileAdmin(admin.ModelAdmin):

    list_display = ('file',)
    search_fields = ('file',)

    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()

admin.site.register(TranslationFile, TranslationFileAdmin)
'''


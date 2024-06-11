from django.urls import path
from .views import Test, ChangeLanguage, UploadTranslation, DownloadTranslation



urlpatterns = [
    #path('', Test.as_view(), name='test'),
    path('change-language', ChangeLanguage.as_view(), name='change_language'),
    path('upload-translation', UploadTranslation.as_view(), name='upload_translation'),
    path('download-translation', DownloadTranslation.as_view(), name='download_translation'),
]
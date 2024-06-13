from django.db.models import Manager
from django.utils.translation import get_language, activate
from rest_framework import generics

AVAILABLE_LANGUAGES = ['uz', 'ru', 'crl']


class TranslatedListView(generics.ListAPIView):
    manager: Manager

    def get_queryset(self):
        self.update_lang()
        return self.manager.all()

    def update_lang(self):
        activate(self.get_language())

    def get_language(self):
        if lang_from_header := self.request.headers.get('accept-language'):
            if lang_from_header and lang_from_header not in AVAILABLE_LANGUAGES:
                lang_from_header = 'ru'

        return lang_from_header or get_language()

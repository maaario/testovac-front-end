import os

from django import forms
from django.utils.translation import ugettext_lazy as _

from . import constants
from . import settings as submit_settings
from .submit_helpers import add_language_preference_to_filename


class FileSubmitForm(forms.Form):
    """
    Reusable form for file uploading.
    Constructor takes additional keyword argument 'configuration' - a dict with parameters.
    """
    def __init__(self, *args, **kwargs):
        config = kwargs.pop('configuration')
        super(FileSubmitForm, self).__init__(*args, **kwargs)

        self.extensions = config.get('extensions', None)
        self.languages = config.get('languages', None)

        if self.languages is not None:
            automatic = [[constants.DEDUCE_LANGUAGE_AUTOMATICALLY_OPTION, constants.DEDUCE_LANGUAGE_AUTOMATICALLY_VERBOSE]]
            self.fields['language'] = forms.ChoiceField(label=_('Language'),
                                                        choices=automatic + self.languages,
                                                        required=True)

    submit_file = forms.FileField(
        max_length=submit_settings.SUBMIT_UPLOADED_FILENAME_MAXLENGTH,
        allow_empty_file=True,
    )

    def clean_submit_file(self):
        sfile = self.cleaned_data.get('submit_file', None)
        if sfile:
            extension = os.path.splitext(sfile.name)[1].lower()
            if self.extensions is not None and extension not in self.extensions:
                raise forms.ValidationError(_('Invalid file extension %(extension)s'),
                                            code='invalid extension',
                                            params={'extension': extension})
            return sfile
        else:
            raise forms.ValidationError(_('No file was submitted'), code='no file')

    def clean(self):
        if 'submit_file' in self.cleaned_data and 'language' in self.cleaned_data and self.languages is not None:
            filename = self.cleaned_data['submit_file'].name
            language = self.cleaned_data['language']
            allowed_languages = map(lambda choice: choice[0], self.languages)

            try:
                self.cleaned_data['submit_file'].name = add_language_preference_to_filename(filename, language, allowed_languages)
            except Exception:
                raise forms.ValidationError(_('Automatic language discovery failed. Unknown language extension.'),
                                            code='invalid language')

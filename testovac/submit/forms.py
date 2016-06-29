from django import forms

import os

from . import settings as submit_settings


class FileSubmitForm(forms.Form):
    """
    Reusable form for file uploading.
    Constructor takes additional keyword argument 'configuration' - an object-dict with parameters.
    """
    def __init__(self, *args, **kwargs):
        config = kwargs.pop('configuration')
        super(FileSubmitForm, self).__init__(*args, **kwargs)

        self.extensions = config.get('extensions', None)
        self.languages = config.get('languages', None)

        if self.languages is not None:
            self.fields['language'] = forms.ChoiceField(label='language', choices=self.languages)

    submit_file = forms.FileField(
        max_length=submit_settings.UPLOADED_FILENAME_MAXLENGTH,
        allow_empty_file=True,
    )

    def clean_submit_file(self):
        sfile = self.cleaned_data['submit_file']
        if sfile:
            extension = os.path.splitext(sfile.name)[1].lower()
            if self.extensions is not None and extension not in self.extensions:
                raise forms.ValidationError('Invalid file extension %s. Only following formats are allowed %s'
                                            % (extension, ' '.join(self.extensions)))
            return sfile
        else:
            raise forms.ValidationError('No file')

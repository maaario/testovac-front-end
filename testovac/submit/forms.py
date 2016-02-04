from django import forms

import os

from . import settings as submit_settings


class FileSubmitForm(forms.Form):
    extensions = None

    submit_file = forms.FileField(
        max_length=submit_settings.UPLOADED_FILENAME_MAXLENGTH,
        allow_empty_file=True,
    )

    def clean_submit_file(self):
        sfile = self.cleaned_data['submit_file']
        if sfile:
            extension = os.path.splitext(sfile.name)[1]
            if self.extensions and extension.lower() not in self.extensions:
                raise forms.ValidationError('Invalid file extension %s' % extension)
            return sfile
        else:
            raise forms.ValidationError('No file')


class SourceSubmitForm(FileSubmitForm):
    LANGUAGE_CHOICES = (
        ('.', 'Automatically'),
        ('.cc', 'C++ (.cpp/.cc)'),
        ('.pas', 'Pascal (.pas/.dpr)'),
        ('.c', 'C (.c)'),
        ('.py', 'Python 3.4 (.py/.py3)'),
        ('.hs', 'Haskell (.hs)'),
        ('.cs', 'C# (.cs)'),
        ('.java', 'Java (.java)')
    )
    language = forms.ChoiceField(label='Language', choices=LANGUAGE_CHOICES)


class DescriptionSubmitForm(FileSubmitForm):
    extensions = submit_settings.SUBMIT_DESCRIPTION_ALLOWED_EXTENSIONS


class TestableZipSubmitForm(FileSubmitForm):
    extensions = ['.zip']

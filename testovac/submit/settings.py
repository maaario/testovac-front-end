from django.conf import settings as django_settings

SUBMIT_PATH = getattr(django_settings, 'SUBMIT_PATH', 'submit/')

# DB can hold names with length up to 128, some space is reserved for extension mapping
SUBMIT_UPLOADED_FILENAME_MAXLENGTH = int(getattr(django_settings, 'SUBMIT_UPLOADED_FILENAME_MAXLENGTH', 120))

# Extensions of uploaded sourcefiles will be replaced for compatibility with judge
# JSON Configs will be validated against VALUES in this dict
SUBMIT_EXTENSION_MAPPING_FOR_JUDGE = getattr(django_settings, 'SUBMIT_EXTENSION_MAPPING_FOR_JUDGE',
    {
        ".cpp": ".cc",
        ".cc": ".cc",
        ".pp": ".pas",
        ".pas": ".pas",
        ".dpr": ".pas",
        ".c": ".c",
        ".py": ".py",
        ".py3": ".py",
        ".hs": ".hs",
        ".cs": ".cs",
        ".java": ".java",
        ".zip": ".zip"
    }
)

SUBMIT_VIEWABLE_EXTENSIONS = getattr(django_settings, 'SUBMIT_VIEWABLE_EXTENSIONS', ('.pdf', '.txt'))

JUDGE_INTERFACE_IDENTITY = getattr(django_settings, 'JUDGE_INTERFACE_IDENTITY', 'TESTOVAC')

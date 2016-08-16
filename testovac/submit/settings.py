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
JUDGE_ADDRESS = getattr(django_settings, 'JUDGE_ADDRESS', '127.0.0.1')
JUDGE_PORT = getattr(django_settings, 'JUDGE_PORT', 12347)

# Override view methods to set `submit.is_accepted` field or submit success message
SUBMIT_POST_SUBMIT_FORM_VIEW = getattr(django_settings, 'SUBMIT_POST_SUBMIT_FORM_VIEW',
                                       'testovac.submit.views.PostSubmitForm')
# Format of displayed score can depend on competition
SUBMIT_DISPLAY_SCORE = getattr(django_settings, 'SUBMIT_DISPLAY_SCORE',
                               'testovac.submit.defaults.display_score')
# Override `SubmitReceiver.__str__()` to be more descriptive than "{}".format(id)
SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME = getattr(django_settings, 'SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME',
                                              'testovac.submit.defaults.display_submit_receiver_name')

JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER = getattr(django_settings, 'JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER',
                                                   'testovac.submit.defaults.default_inputs_folder_at_judge')

# Override these functions to set access rights for receivers
SUBMIT_CAN_POST_SUBMIT = getattr(django_settings, 'SUBMIT_CAN_POST_SUBMIT',
                                 'testovac.submit.defaults.can_post_submit')
SUBMIT_HAS_ADMIN_PRIVILEGES_FOR_RECEIVER = getattr(django_settings, 'SUBMIT_HAS_ADMIN_PRIVILEGES_FOR_RECEIVER',
                                                   'testovac.submit.defaults.has_admin_privileges_for_receiver')

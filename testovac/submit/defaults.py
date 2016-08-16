from . import settings as submit_settings


def display_score(review):
    return str(review.score)


def submit_receiver_type(receiver):
    if receiver.configuration.get('send_to_judge', False):
        return 'source'
    if 'link' in receiver.configuration:
        return 'link'
    if 'form' in receiver.configuration:
        return 'description'
    return 'other'


def display_submit_receiver_name(receiver):
    return '{} ({})'.format(receiver.id, submit_receiver_type(receiver))


def default_inputs_folder_at_judge(receiver):
    return '{}-{}'.format(submit_settings.JUDGE_INTERFACE_IDENTITY, receiver.id)


def can_post_submit(receiver, user):
    return True


def has_admin_privileges_for_receiver(receiver, user):
    return user.is_staff

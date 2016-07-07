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

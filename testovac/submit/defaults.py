def display_score(review):
    return str(review.score)


def display_submit_receiver_name(receiver):
    if receiver.configuration.get('send_to_judge', False):
        receiver_type = 'source'
    elif 'link' in receiver.configuration:
        receiver_type = 'link'
    elif 'form' in receiver.configuration:
        receiver_type = 'description'
    else:
        receiver_type = 'other'

    return '{} ({})'.format(receiver.id, receiver_type)

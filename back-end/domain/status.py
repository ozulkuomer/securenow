from helpers.data_access import run, run_non_query

def create_status(object):
    text = object['text']
    user_id = object['user_id']
    inserted_row = None
    if text and user_id:
        inserted_row = run_non_query('insert into statuses (text, user_id) values (%(text)s, %(user_id)s);', {'text':text, 'user_id':user_id})
        if inserted_row == 0:
            raise NameError('Create Status Error')


def get_status_list():
    result = run('SELECT text, user_id, _id FROM statuses ORDER BY _id DESC')
    return result

def validate_status(object):
    text = None
    user_id = None
    if object:
        if 'text' in object:
            text = object['text']
        if 'user_id' in object:
            user_id = object['user_id']
    
    if not text:
        yield 'Text is required'

    if not user_id:
        yield 'User Id is required'

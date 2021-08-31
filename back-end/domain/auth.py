from helpers.data_access import run

def validate_login(object):
    email = None
    password = None
    if object:
        if 'email' in object:
            email = object['email']
        if 'password' in object:
            password = object['password']
    
    if not email:
        yield 'email is required'

    if not password:
        yield 'password is required'

def get_user_id(request_data):
    email = request_data['email']
    try:
        result = run('SELECT user_id FROM auths WHERE email=%(email)s', {'email':email})
        if len(result) == 1:
            return result[0]['user_id']
    except Exception as ex:
        print('get user id err', ex)
    return None

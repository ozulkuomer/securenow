from helpers.data_access import run

def get_user(user_id):
    try:
        result = run('SELECT _id, username, email FROM users WHERE _id = %(user_id)s', {'user_id':user_id})
        return result[0]
    except Exception as ex:
        print('get user id err', ex)
    return None

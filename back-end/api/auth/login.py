from domain.user import get_user
from domain.auth import validate_login, get_user_id
from helpers.helpers import get_api_response
from flask import  make_response


def login(request_data):
    try:
        validation_list = list(validate_login(request_data))
        if( len(validation_list) > 0):
            return get_api_response(validation_list), 400
        user_id = get_user_id(request_data)
        if not user_id:
            return 'Wrong email or password', 400
        user = get_user(user_id)
        if user:
            body = get_api_response([user])
            response = make_response(body)
            response.set_cookie('user_id', str(user_id), httponly=True, max_age=60*60)
            response.status_code = 200
            return response
    except Exception as ex:
        print('Login error', ex)
    
    return 'BadRequest', 400


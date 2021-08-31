from domain.status import get_status_list, create_status, validate_status
from helpers.helpers import get_api_response


def post_status(request_data):
    try:
        validation_list = list(validate_status(request_data))
        if( len(validation_list) > 0):
            return get_api_response(validation_list), 400

        create_status(request_data)
        return 'Created'

    except Exception as ex:
        print('Create Status error', ex)
    
    return 'BadRequest', 400


def get_status():
    try:
        rows = get_status_list()
        return get_api_response(rows)
    except Exception as ex:
        print('Status list err', ex)
        
    return 'BadRequest', 400

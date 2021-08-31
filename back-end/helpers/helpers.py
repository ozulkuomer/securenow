import json

def get_api_response(obj):
    return json.dumps({'payload' : obj})
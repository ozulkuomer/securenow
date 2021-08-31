from helpers.helpers import get_api_response
from domain.user import get_user
from flask import Flask
from flask_cors import CORS
from flask import request
from api.status.status import post_status, get_status
from api.auth.login import login



app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#API/User Begin

@app.route('/api/user', methods = ['GET'])
def api_user_user_id_get():
    return get_api_response([get_user(1)])

#API/User  End


#API/AUTH Begin

@app.route('/api/auth/login', methods = ['POST'])
def api_auth_login_post():
    return login(request.get_json())
    

#API/AUTH End



# API/STATUS Begin

@app.route('/api/status', methods = ['POST'])
def api_status_post():
    return post_status(request.get_json())

@app.route('/api/status', methods = ['GET'])
def api_status_get():
    return get_status()


# API/STATUS End

if __name__ == '__main__':
    app.run(debug=True)
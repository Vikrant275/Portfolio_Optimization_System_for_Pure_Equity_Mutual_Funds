from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token,verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash

'''
generate_password_hash: 
It takes a plain password (e.g., "MySecret123") and turns it into a long, scrambled string of gibberish. Even if a hacker steals your database, they won't know the real password.
check_password_hash: 
When a user tries to log in, this compares the password they just typed with the scrambled one in your database to see if they match
'''

'''
create_access_token: 
It creates a JWT (JSON Web Token). Think of this as a digital "VIP Wristband."
The server gives this token to the user's browser.
For every future request (like checking stock history), the browser "shows" this token to the server.
The server sees the token and says, "I recognize this; you are authorized
'''

from fetch_servers.config import Config


auth_bp = Blueprint('auth',__name__)


# for sample
user_db = {
    'vikrant':generate_password_hash('password123'),
    'admin' : generate_password_hash('admin123')
}

@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username not in user_db:
        return {'error':'Invalid username'}, 401
    if not check_password_hash(user_db[username],password):
        return {'error':'Invalid password'}, 401

    #crate JWT token
    token = create_access_token(identity=username)

    return jsonify({'token':token})

# auth check
def authenticate():
    try:
        verify_jwt_in_request()
    except:
        #fallback api
        key = request.headers.get('x-api-key')
        if key != Config.API_KEY:
            abort(401,description="Invalid API Key ...Unauthorized")



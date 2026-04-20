from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import sys

from fetch_servers.config import Config
from fetch_servers.Audit_Server.api.audit_api import audit_bp
from fetch_servers.Risk_Server.api.risk_api import risk_bp
from fetch_servers.auth_user import auth_bp
from framework.logger import logging
from framework.exception import MyException

def create_app():
    try:
        app = Flask(__name__)
        app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET

        logging.info("Config loaded")

        JWTManager(app)

        #Rate Limiter
        limiter = Limiter(
            key_func = get_remote_address,
            default_limits = [Config.RATE_LIMIT]
        )
        limiter.init_app(app)


        #Register APIs
        app.register_blueprint(auth_bp)
        app.register_blueprint(risk_bp)
        app.register_blueprint(audit_bp)

        @app.before_request
        def log_request():
            logging.info('Incoming request')

        @app.errorhandler(401)
        def unauthorized(e):
            logging.warn('Unauthorized')
            return {'error': 'Unauthorized'}, 401

        return app

    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0',port=5000,debug=True)



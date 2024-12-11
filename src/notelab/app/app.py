import logging
from functools import wraps
from flask import Flask, request
from flask_restx import Api
from flask_talisman import Talisman
from utils.app_logger import setup_logger
from utils.app_config import Config
from notelab.app.routes import db_routes

config = Config()

app = Flask(__name__)
flask_api = Api(app, doc='/', title='NoteLab API', version='1.0', description='API for NoteLab')

csp = {
    'default-src': ["'self'"],
    'style-src': ["'self'", "'unsafe-inline'"],
    'script-src': ["'self'", "'unsafe-inline'"]
}

# Force HTTPS
app.config['TALISMAN_FORCE_HTTPS'] = True
app.config['FLASK_URL'] = f'https://{config.host}:{config.server_port}'
Talisman(app, content_security_policy=csp)

logger = setup_logger('app')
app.logger.handlers = logger.handlers

db_routes.init_routes(flask_api)

# Log all registered routes
if not hasattr(app, 'routes_logged'):
    for rule in app.url_map.iter_rules():
        app.logger.info(f"Registered route: {rule}")
    app.routes_logged = True

# Custom decorator to log route access with more details
def log_route_access(log_level=logging.INFO, log_headers=False, log_body=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Log basic request information
            log_msg = f"Accessed route: {request.path}, Method: {request.method}"

            # Log request headers
            if log_headers:
                log_msg += f", Headers: {dict(request.headers)}"

            # Log request body (only for POST/PUT requests)
            if log_body and request.data:
                log_msg += f", Body: {request.data.decode('utf-8')}"

            app.logger.log(log_level, log_msg)

            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    app.run(debug=True)

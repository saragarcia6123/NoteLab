import logging
import os
from functools import wraps
import flask
from flask import Flask, request, redirect
from flask_restx import Api
from flask_talisman import Talisman
from notelab.app.routes import db_routes
from notelab.utils.app_config import AppConfig
from notelab.utils.app_logger import setup_logger

config = AppConfig()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
api_bp = flask.Blueprint("api", __name__, url_prefix="/api/")
api = Api(
    api_bp, version='1.0', title='NoteLab API',
    description='API for NoteLab',
    doc='/docs'
)

app.register_blueprint(api_bp)

# Content Security Policy for Talisman
# Only allow resources from the same origin and inline styles/scripts
# NOT RECOMMENDED FOR PRODUCTION
csp = {
    'default-src': ["'self'"],
    'style-src': ["'self'", "'unsafe-inline'"],
    'script-src': ["'self'", "'unsafe-inline'"]
}

# Force HTTPS for all requests
app.config['TALISMAN_FORCE_HTTPS'] = True
app.config['FLASK_URL'] = f'https://{config.host}:{config.server_port}'
Talisman(app, content_security_policy=csp)

logger = setup_logger('App')
app.logger.handlers = logger.handlers

db_routes.init_routes(api)

# Log all registered routes
routes_logged = False
if not routes_logged:
    for rule in app.url_map.iter_rules():
        app.logger.info(f"Registered route: {rule}")
    routes_logged = True

reload_detected = False

@app.before_request
def before_request():
    global reload_detected
    if 'werkzeug.server.shutdown' in request.environ:
        reload_detected = True

@app.after_request
def after_request(response):
    global reload_detected
    if reload_detected:
        app.logger.info("Application reloaded")
        reload_detected = False
    return response

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

@app.route('/')
def redirect_to_docs():
    return redirect('/api/docs')

if __name__ == "__main__":
    app.run(debug=True, host=config.host, port=config.server_port, ssl_context=(os.getenv('SSL_CERT_FILE'), os.getenv('SSL_KEY_FILE')))

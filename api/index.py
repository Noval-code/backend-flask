from .extensions import mongo  # kalau extensions.py satu folder
from flask import Flask, jsonify, request
from flask_cors import CORS
from .config import DevelopmentConfig
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from routes.decorators import require_api_key
import logging

# Blueprints
from routes.auth_routes import auth_bp
from routes.article_routes import article_bp
from routes.progress_routes import progress_bp
from routes.analysis_routes import analysis_bp

# Logging
logging.basicConfig(level=logging.DEBUG)

# Inisialisasi App
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['STATIC_API_KEY'] = '1234567890abcdef'
CORS(app)

# Inisialisasi Mongo, JWT, Mail
mongo.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)
revoked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens

# Register Blueprints
app.register_blueprint(analysis_bp)
app.register_blueprint(article_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(progress_bp, url_prefix='/api')

# Routes
@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "Welcome to the API"}), 200

@app.route('/secure-data', methods=['GET'])
@require_api_key
def secure_data():
    return jsonify({"message": "API Key is valid, access granted!"})

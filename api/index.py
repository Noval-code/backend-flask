# api/index.py

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
import logging

# Import konfigurasi dan ekstensi
from config import DevelopmentConfig, ProductionConfig
from extensions import mongo
from routes.decorators import require_api_key

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.article_routes import article_bp
from routes.progress_routes import progress_bp
from routes.analysis_routes import analysis_bp

# Logging
logging.basicConfig(level=logging.DEBUG)

# Inisialisasi app Flask
app = Flask(__name__)

# Set API Key statis jika digunakan
app.config['STATIC_API_KEY'] = '1234567890abcdef'

# Setup ekstensi
CORS(app)
mongo.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)
revoked_tokens = set()

# Token blacklist handler
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(article_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(progress_bp, url_prefix="/api")

# Routes dasar
@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the API"}), 200

@app.route("/secure-data", methods=["GET"])
@require_api_key
def secure_data():
    return jsonify({"message": "API Key is valid, access granted!"})

# Handler untuk Vercel (penting!)
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

print("=== DEBUG ENV ===")
print("SECRET_KEY:", os.environ.get("SECRET_KEY"))
print("MONGO_URI:", os.environ.get("MONGO_URI"))
print("=================")
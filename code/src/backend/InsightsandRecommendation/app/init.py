import os
from flask import Flask

from config import Config
from flask_cors import CORS
from datetime import timedelta
from db.init import init_db

db_client = None

def create_app():
    app = Flask(__name__)
    CORS(app)
    global db_client
    db_client = init_db()

    from app.APIs.RunAdaptiveAnalytics import run_adaptive_analytics_bp
    from app.APIs.GenerateInitialInsights import initial_insight_generation_bp

    app.secret_key = os.urandom(24)  # Use a strong secret key in production
    app.permanent_session_lifetime = timedelta(days=5)  # Set session lifetime
    app.config.from_object(Config)
    app.register_blueprint(run_adaptive_analytics_bp)
    app.register_blueprint(initial_insight_generation_bp)
    return app

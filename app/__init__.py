# app/__init__.py
from flask import Flask
from app.extensions import db
from app.config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route("/ping")
    def ping():
        return {"ok": True, "db": "connected"}

    return app

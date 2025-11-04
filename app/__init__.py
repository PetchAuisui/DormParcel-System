from flask import Flask
from app.extensions import db
from app.config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.models.user_model import User
    from app.models.dormitory_model import Dormitory

    from app.controllers.main_controller import bp as main_bp
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    @app.route("/ping")
    def ping():
        return {"ok": True, "db": "connected"}

    return app

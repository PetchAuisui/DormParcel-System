
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# สร้าง object ของ SQLAlchemy
db = SQLAlchemy()

def create_app():
    load_dotenv()  # โหลดค่าจากไฟล์ .env
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    # นำเข้า routes (ซึ่งมี blueprint)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

app = create_app()

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "dorm_parcel"}

    user_id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.dormitories.dorm_id"), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.rooms.room_id"), nullable=True)
    full_name = db.Column(db.String(120), nullable=False)
    national_id = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="RESIDENT")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"

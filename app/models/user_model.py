from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "dorm_parcel"}

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    national_id = db.Column(db.String(13), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="RESIDENT")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    dorm_roles = db.relationship("UserDormRole", back_populates="user", cascade="all, delete-orphan")
    room_assignments = db.relationship("UserRoomAssignment", back_populates="user", cascade="all, delete-orphan")
    parcels_received = db.relationship("Parcel", back_populates="receiver", foreign_keys="Parcel.receiver_id")
    parcels_checked_in = db.relationship("Parcel", back_populates="received_by_user", foreign_keys="Parcel.received_by")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.user_id} {self.full_name}>"

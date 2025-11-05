from app.extensions import db

class Dormitory(db.Model):
    __tablename__ = "dormitories"
    __table_args__ = {"schema": "dorm_parcel"}

    dorm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text)
    building_code = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    total_floors = db.Column(db.Integer, default=1)
    total_rooms = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    rooms = db.relationship("Room", back_populates="dormitory", cascade="all, delete-orphan")
    user_roles = db.relationship("UserDormRole", back_populates="dorm", cascade="all, delete-orphan")
    parcels = db.relationship("Parcel", back_populates="dorm", cascade="all, delete-orphan")

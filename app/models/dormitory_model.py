from app.extensions import db

class Dormitory(db.Model):
    __tablename__ = "dormitories"
    __table_args__ = {"schema": "dorm_parcel"}

    dorm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    total_floors = db.Column(db.Integer, default=1)
    total_rooms = db.Column(db.Integer, default=0)
    google_map_link = db.Column(db.Text)  # ✅ เพิ่มตรงนี้
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    rooms = db.relationship("Room", back_populates="dormitory", lazy=True)
    users = db.relationship("User", back_populates="dormitory", lazy=True)
    user_roles = db.relationship("UserDormRole", back_populates="dormitory", lazy=True)
    parcels = db.relationship("Parcel", back_populates="dormitory", lazy=True)

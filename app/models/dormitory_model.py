from app.extensions import db

class Dormitory(db.Model):
    __tablename__ = "dormitories"
    __table_args__ = {"schema": "dorm_parcel"}

    dorm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text)
    building_code = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

from app.extensions import db

class Carrier(db.Model):
    __tablename__ = "carriers"
    __table_args__ = {"schema": "dorm_parcel"}

    carrier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    parcels = db.relationship("Parcel", back_populates="carrier")

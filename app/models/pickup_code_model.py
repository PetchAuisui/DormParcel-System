from app.extensions import db

class PickupCode(db.Model):
    __tablename__ = "pickup_codes"
    __table_args__ = {"schema": "dorm_parcel"}

    code_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.parcels.parcel_id", ondelete="CASCADE"), unique=True)
    code_hash = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    parcel = db.relationship("Parcel", back_populates="pickup_code")

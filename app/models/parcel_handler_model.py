from app.extensions import db

class ParcelHandler(db.Model):
    __tablename__ = "parcel_handlers"
    __table_args__ = {"schema": "dorm_parcel"}

    parcel_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.parcels.parcel_id", ondelete="CASCADE"), primary_key=True)
    handler_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="CASCADE"), primary_key=True)
    role_in_process = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    parcel = db.relationship("Parcel", back_populates="handlers")
    handler = db.relationship("User")

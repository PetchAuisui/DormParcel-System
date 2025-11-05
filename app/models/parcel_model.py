from app.extensions import db

class Parcel(db.Model):
    __tablename__ = "parcels"
    __table_args__ = {"schema": "dorm_parcel"}

    parcel_id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.dormitories.dorm_id", ondelete="CASCADE"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="SET NULL"))
    carrier_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.carriers.carrier_id", ondelete="SET NULL"))
    received_by = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="SET NULL"))

    tracking_code = db.Column(db.String(100), unique=True, nullable=False)
    sender_name = db.Column(db.String(120))
    sender_phone = db.Column(db.String(20))
    parcel_image_url = db.Column(db.Text)
    size = db.Column(db.String(50))
    storage_bin = db.Column(db.String(40))
    note = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)
    received_at = db.Column(db.DateTime)
    picked_up_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    dormitory = db.relationship("Dormitory", back_populates="parcels")
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="received_parcels")
    carrier = db.relationship("Carrier", back_populates="parcels")
    handlers = db.relationship("ParcelHandler", back_populates="parcel", lazy=True)
    history = db.relationship("ParcelStatusHistory", back_populates="parcel", lazy=True)
    pickup_code = db.relationship("PickupCode", back_populates="parcel", uselist=False, lazy=True)
    notifications = db.relationship("Notification", back_populates="parcel", lazy=True)

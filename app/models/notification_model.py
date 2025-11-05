from app.extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"
    __table_args__ = {"schema": "dorm_parcel"}

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="CASCADE"))
    parcel_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.parcels.parcel_id", ondelete="CASCADE"))
    channel = db.Column(db.String(20))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    parcel = db.relationship("Parcel", back_populates="notifications")

from app.extensions import db

class ParcelStatusHistory(db.Model):
    __tablename__ = "parcel_status_history"
    __table_args__ = {"schema": "dorm_parcel"}

    history_id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.parcels.parcel_id", ondelete="CASCADE"))
    changed_by = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="SET NULL"))
    from_status = db.Column(db.String(20))
    to_status = db.Column(db.String(20))
    remark = db.Column(db.Text)
    changed_at = db.Column(db.DateTime, server_default=db.func.now())

    parcel = db.relationship("Parcel", back_populates="history")
    changed_by_user = db.relationship("User", back_populates="parcel_status_changes")

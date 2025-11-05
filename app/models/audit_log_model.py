from app.extensions import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "dorm_parcel"}

    audit_id = db.Column(db.Integer, primary_key=True)
    actor_user_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="SET NULL"))
    action = db.Column(db.String(50), nullable=False)
    target_type = db.Column(db.String(50))
    target_id = db.Column(db.Integer)
    meta = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    actor = db.relationship("User", back_populates="audit_logs")

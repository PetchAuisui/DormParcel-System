from app.extensions import db
from datetime import datetime
from app.models import SCHEMA

class OfficerDorm(db.Model):
    __tablename__ = "officer_dorms"
    __table_args__ = {"schema": SCHEMA}

    officer_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.users.user_id", ondelete="CASCADE"), primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.dormitories.dorm_id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    officer = db.relationship("User", back_populates="officer_dorms")
    dormitory = db.relationship("Dormitory", back_populates="officers")

    def __repr__(self):
        return f"<OfficerDorm officer={self.officer_id} dorm={self.dorm_id}>"

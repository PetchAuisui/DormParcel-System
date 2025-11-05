from app.extensions import db
from datetime import datetime
from app.models import SCHEMA

class DormStaff(db.Model):
    __tablename__ = "dorm_staffs"
    __table_args__ = {"schema": SCHEMA}

    staff_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.users.user_id", ondelete="CASCADE"), primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.dormitories.dorm_id", ondelete="CASCADE"), primary_key=True)
    position = db.Column(db.String(50))
    hired_at = db.Column(db.DateTime, default=datetime.utcnow)

    staff = db.relationship("User", back_populates="staffed_dorms")
    dormitory = db.relationship("Dormitory", back_populates="staffs")

    def __repr__(self):
        return f"<DormStaff user={self.staff_id} dorm={self.dorm_id}>"

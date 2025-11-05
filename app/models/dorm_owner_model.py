from app.extensions import db
from datetime import datetime
from app.models import SCHEMA

class DormOwner(db.Model):
    __tablename__ = "dorm_owners"
    __table_args__ = {"schema": SCHEMA}

    owner_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.users.user_id", ondelete="CASCADE"), primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.dormitories.dorm_id", ondelete="CASCADE"), primary_key=True)
    since = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship("User", back_populates="owned_dorms")
    dormitory = db.relationship("Dormitory", back_populates="owners")

    def __repr__(self):
        return f"<DormOwner user={self.owner_id} dorm={self.dorm_id}>"

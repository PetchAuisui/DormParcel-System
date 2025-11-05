from app.extensions import db
from datetime import datetime
from app.models import SCHEMA

class ParcelOfficer(db.Model):
    __tablename__ = "parcel_officers"
    __table_args__ = {"schema": SCHEMA}

    parcel_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.parcels.parcel_id", ondelete="CASCADE"), primary_key=True)
    officer_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.users.user_id", ondelete="CASCADE"), primary_key=True)
    role_in_process = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    parcel = db.relationship("Parcel", back_populates="officers")
    officer = db.relationship("User", back_populates="handled_parcels")

    def __repr__(self):
        return f"<ParcelOfficer parcel={self.parcel_id} officer={self.officer_id}>"

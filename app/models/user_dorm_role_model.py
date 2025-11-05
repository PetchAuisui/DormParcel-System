from app.extensions import db

class UserDormRole(db.Model):
    __tablename__ = "user_dorm_roles"
    __table_args__ = {"schema": "dorm_parcel"}

    user_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.users.user_id", ondelete="CASCADE"), primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.dormitories.dorm_id", ondelete="CASCADE"), primary_key=True)
    role_in_dorm = db.Column(db.String(20), primary_key=True)
    assigned_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", back_populates="dorm_roles")
    dormitory = db.relationship("Dormitory", back_populates="user_roles")

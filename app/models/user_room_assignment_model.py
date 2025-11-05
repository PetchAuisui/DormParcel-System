from app.extensions import db

class UserRoomAssignment(db.Model):
    __tablename__ = "user_room_assignments"
    __table_args__ = {"schema": "dorm_parcel"}

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("dorm_parcel.users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    room_id = db.Column(
        db.Integer,
        db.ForeignKey("dorm_parcel.rooms.room_id", ondelete="CASCADE"),
        primary_key=True
    )
    move_in = db.Column(db.Date)
    move_out = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship("User", back_populates="room_assignments")
    room = db.relationship("Room", back_populates="user_assignments")

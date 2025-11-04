from app.extensions import db

class Room(db.Model):
    __tablename__ = "rooms"
    __table_args__ = {"schema": "dorm_parcel"}

    room_id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.dormitories.dorm_id"))
    room_number = db.Column(db.String(20))
    floor = db.Column(db.Integer)
    type = db.Column(db.String(50))
    status = db.Column(db.String(20), default="AVAILABLE")


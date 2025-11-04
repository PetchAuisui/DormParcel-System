from app.extensions import db

# import models
from app.models.dormitory_model import Dormitory
from app.models.room_model import Room
from app.models.user_model import User

Dormitory.rooms = db.relationship("Room", backref="dormitory", lazy=True)
Dormitory.users = db.relationship("User", backref="dormitory", lazy=True)
Room.users = db.relationship("User", backref="room", lazy=True)

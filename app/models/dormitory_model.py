from app.extensions import db

class Dormitory(db.Model):
    __tablename__ = "dormitories"   
    dorm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    building_code = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    users = db.relationship("User", backref="dormitory", lazy=True)

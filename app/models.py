from app.extensions import db
from datetime import datetime

# ---------- Dormitory ----------
class Dormitory(db.Model):
    __tablename__ = "dormitories"

    dorm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(120))
    building_code = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    users = db.relationship("User", backref="dormitory", lazy=True)
    parcels = db.relationship("Parcel", backref="dormitory", lazy=True)

    def __repr__(self):
        return f"<Dormitory {self.name}>"

# ---------- User ----------
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dormitories.dorm_id"), nullable=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    room_number = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    parcels = db.relationship("Parcel", backref="receiver", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"

# ---------- Carrier ----------
class Carrier(db.Model):
    __tablename__ = "carriers"

    carrier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    parcels = db.relationship("Parcel", backref="carrier", lazy=True)

    def __repr__(self):
        return f"<Carrier {self.name}>"

# ---------- Parcel ----------
class Parcel(db.Model):
    __tablename__ = "parcels"

    parcel_id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dormitories.dorm_id"))
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.carrier_id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    tracking_code = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    storage_bin = db.Column(db.String(40))
    note = db.Column(db.Text)
    received_at = db.Column(db.DateTime)
    picked_up_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Parcel {self.tracking_code} - {self.status}>"

# ---------- Notification ----------
class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    parcel_id = db.Column(db.Integer, db.ForeignKey("parcels.parcel_id"))
    channel = db.Column(db.String(20))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.notification_id} to User {self.user_id}>"

# ---------- Audit Log ----------
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    audit_id = db.Column(db.Integer, primary_key=True)
    actor_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    action = db.Column(db.String(40), nullable=False)
    target_type = db.Column(db.String(40))
    target_id = db.Column(db.Integer)
    meta = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Audit {self.action} by {self.actor_user_id}>"

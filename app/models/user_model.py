from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "dorm_parcel"}

    user_id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.dormitories.dorm_id", ondelete="SET NULL"))
    room_id = db.Column(db.Integer, db.ForeignKey("dorm_parcel.rooms.room_id", ondelete="SET NULL"))

    full_name = db.Column(db.String(120), nullable=False)
    national_id = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    dormitory = db.relationship("Dormitory", back_populates="users")
    room = db.relationship("Room", back_populates="users")

    dorm_roles = db.relationship("UserDormRole", back_populates="user", lazy=True)
    received_parcels = db.relationship("Parcel", foreign_keys="[Parcel.receiver_id]", back_populates="receiver", lazy=True)
    handled_parcels = db.relationship("ParcelHandler", back_populates="handler", lazy=True)
    parcel_status_changes = db.relationship("ParcelStatusHistory", back_populates="changed_by_user", lazy=True)
    notifications = db.relationship("Notification", back_populates="user", lazy=True)
    audit_logs = db.relationship("AuditLog", back_populates="actor", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

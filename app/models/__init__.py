from app.extensions import db
from app.models.user_model import User
from app.models.dormitory_model import Dormitory
from app.models.room_model import Room
from app.models.user_dorm_role_model import UserDormRole
from app.models.carrier_model import Carrier
from app.models.parcel_model import Parcel
from app.models.parcel_handler_model import ParcelHandler
from app.models.parcel_status_history_model import ParcelStatusHistory
from app.models.pickup_code_model import PickupCode
from app.models.notification_model import Notification
from app.models.audit_log_model import AuditLog

db.configure_mappers()

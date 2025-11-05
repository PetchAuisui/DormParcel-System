from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

from app.extensions import db
from app.models.room_model import Room
from app.models.dormitory_model import Dormitory

bp = Blueprint("admin_room", __name__, url_prefix="/admin/rooms")


class RoomForm(FlaskForm):
    room_number = StringField("หมายเลขห้อง", validators=[DataRequired(), Length(max=20)])
    floor = IntegerField("ชั้น", validators=[DataRequired(), NumberRange(min=1)])
    type = StringField("ประเภทห้อง", validators=[Length(max=50)])
    status = SelectField(
        "สถานะห้อง",
        choices=[("AVAILABLE", "ว่าง"), ("OCCUPIED", "มีผู้พัก"), ("MAINTENANCE", "ซ่อมแซม")],
        default="AVAILABLE"
    )
    submit = SubmitField("บันทึก")


@bp.before_request
def require_admin_role():
    if session.get("role") != "ADMIN":
        flash("คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "error")
        return redirect(url_for("auth.login"))



bp = Blueprint("admin", __name__, url_prefix="/admin/dorms")


@bp.route("/")
def dorm_list():
    dorms = Dormitory.query.all()
    if not dorms:
        flash("ยังไม่มีข้อมูลหอพัก", "warning")
    return render_template("admin_dorm_list.html", dorms=dorms)


@bp.route("/<int:dorm_id>/rooms")
def dorm_rooms(dorm_id):
    dorm = Dormitory.query.get_or_404(dorm_id)
    rooms = Room.query.filter_by(dorm_id=dorm_id).order_by(Room.floor, Room.room_number).all()
    return render_template("admin_room_list.html", dorm=dorm, rooms=rooms)


from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.dormitory_model import Dormitory

bp = Blueprint("admin", __name__, url_prefix="/admin/dorms")


# 🏢 แสดงรายการหอพักทั้งหมด
@bp.route("/")
def dorm_list():
    dorms = Dormitory.query.order_by(Dormitory.dorm_id.asc()).all()
    if not dorms:
        flash("ยังไม่มีข้อมูลหอพัก", "warning")
    return render_template("admin_dorm_list.html", dorms=dorms)


# ➕ เพิ่มหอพักใหม่
@bp.route("/add", methods=["GET", "POST"])
def add_dorm():
    if request.method == "POST":
        name = request.form.get("name")
        building_code = request.form.get("building_code")
        address = request.form.get("address")
        phone = request.form.get("phone")
        total_floors = request.form.get("total_floors", type=int)
        total_rooms = request.form.get("total_rooms", type=int)

        # ✅ ตรวจสอบข้อมูลที่จำเป็น
        if not name or not building_code:
            flash("กรุณากรอกชื่อหอพักและรหัสอาคาร", "error")
            return redirect(url_for("admin.add_dorm"))

        # ✅ ตรวจรหัสอาคารซ้ำ
        existing = Dormitory.query.filter_by(building_code=building_code).first()
        if existing:
            flash("รหัสอาคารนี้มีอยู่แล้ว ❌", "error")
            return redirect(url_for("admin.add_dorm"))

        new_dorm = Dormitory(
            name=name,
            building_code=building_code,
            address=address,
            phone=phone,
            total_floors=total_floors or 1,
            total_rooms=total_rooms or 0
        )

        db.session.add(new_dorm)
        db.session.commit()
        flash(f"เพิ่มหอพัก {name} เรียบร้อย ✅", "success")
        return redirect(url_for("admin.dorm_list"))

    return render_template("admin_dorm_add.html")


@bp.route("/<int:room_id>/edit", methods=["GET", "POST"])
def room_edit(room_id):
    room = Room.query.get_or_404(room_id)
    form = RoomForm(obj=room)

    if form.validate_on_submit():
        room.room_number = form.room_number.data
        room.floor = form.floor.data
        room.type = form.type.data
        room.status = form.status.data
        db.session.commit()
        flash("อัปเดตข้อมูลห้องเรียบร้อย ✅", "success")
        return redirect(url_for("admin_room.room_list", dorm_id=room.dorm_id))

    return render_template("admin_room_edit.html", form=form, room=room)


@bp.route("/<int:room_id>/delete", methods=["POST"])
def room_delete(room_id):
    room = Room.query.get_or_404(room_id)
    dorm_id = room.dorm_id
    db.session.delete(room)
    db.session.commit()
    flash(f"ลบห้อง {room.room_number} เรียบร้อย ✅", "success")
    return redirect(url_for("admin_room.room_list", dorm_id=dorm_id))

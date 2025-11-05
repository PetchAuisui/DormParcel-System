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

-
@bp.before_request
def require_admin_role():
    if session.get("role") != "ADMIN":
        flash("คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "error")
        return redirect(url_for("auth.login"))


@bp.route("/")
def room_list():
    dorm_id = request.args.get("dorm_id", type=int)
    if not dorm_id:
        flash("กรุณาเลือกหอพักก่อน", "warning")
        return redirect(url_for("admin.dorm_list"))

    dorm = Dormitory.query.get_or_404(dorm_id)
    rooms = Room.query.filter_by(dorm_id=dorm_id).order_by(Room.floor, Room.room_number).all()
    return render_template("admin_room_list.html", dorm=dorm, rooms=rooms)


@bp.route("/add", methods=["GET", "POST"])
def room_add():
    dorm_id = request.args.get("dorm_id", type=int)
    dorm = Dormitory.query.get_or_404(dorm_id)
    form = RoomForm()

    if form.validate_on_submit():
        new_room = Room(
            dorm_id=dorm.dorm_id,
            room_number=form.room_number.data,
            floor=form.floor.data,
            type=form.type.data,
            status=form.status.data,
        )
        db.session.add(new_room)
        db.session.commit()
        flash(f"เพิ่มห้อง {new_room.room_number} ใน {dorm.name} เรียบร้อย ✅", "success")
        return redirect(url_for("admin_room.room_list", dorm_id=dorm_id))

    return render_template("admin_room_add.html", form=form, dorm=dorm)


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

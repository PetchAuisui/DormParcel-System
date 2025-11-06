from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.dormitory_model import Dormitory

bp = Blueprint("admin_dorm", __name__, url_prefix="/admin/dorms")


# 🧱 ตรวจสอบสิทธิ์ก่อนเข้าทุก route
@bp.before_request
def require_admin_role():
    if session.get("role") != "ADMIN":
        flash("คุณไม่มีสิทธิ์เข้าถึงหน้านี้ ❌", "error")
        return redirect(url_for("auth.login"))


@bp.route("/")
def dorm_list():
    dorms = Dormitory.query.order_by(Dormitory.dorm_id.asc()).all()
    if not dorms:
        flash("ยังไม่มีข้อมูลหอพัก", "warning")
    return render_template("admin_dorm_list.html", dorms=dorms)


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
            return redirect(url_for("admin_dorm.add_dorm"))

        # ✅ ตรวจรหัสอาคารซ้ำ
        existing = Dormitory.query.filter_by(building_code=building_code).first()
        if existing:
            flash("รหัสอาคารนี้มีอยู่แล้ว ❌", "error")
            return redirect(url_for("admin_dorm.add_dorm"))

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
        return redirect(url_for("admin_dorm.dorm_list"))

    return render_template("admin_dorm_add.html")

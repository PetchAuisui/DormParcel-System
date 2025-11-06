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
        address = request.form.get("address")
        phone = request.form.get("phone")
        total_floors = request.form.get("total_floors", type=int)
        total_rooms = request.form.get("total_rooms", type=int)
        google_map_link = request.form.get("google_map_link")

        new_dorm = Dormitory(
            name=name,
            address=address,
            phone=phone,
            total_floors=total_floors or 1,
            total_rooms=total_rooms or 0,
            google_map_link=google_map_link,
        )

        db.session.add(new_dorm)
        db.session.commit()
        flash(f"เพิ่มหอพัก {name} เรียบร้อย ✅", "success")
        return redirect(url_for("admin_dorm.dorm_list"))

    return render_template("admin_dorm_add.html")

@bp.route("/<int:dorm_id>/edit", methods=["GET", "POST"])
def edit_dorm(dorm_id):
    dorm = Dormitory.query.get_or_404(dorm_id)

    if request.method == "POST":
        dorm.name = request.form.get("name")
        dorm.address = request.form.get("address")
        dorm.phone = request.form.get("phone")
        dorm.total_floors = request.form.get("total_floors", type=int)
        dorm.total_rooms = request.form.get("total_rooms", type=int)
        # ถ้ามี google_map_link ใน model แล้ว:
        if hasattr(dorm, "google_map_link"):
            dorm.google_map_link = request.form.get("google_map_link")

        try:
            db.session.commit()
            flash(f"แก้ไขข้อมูลหอพัก {dorm.name} เรียบร้อย ✅", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"เกิดข้อผิดพลาดในการบันทึก: {str(e)}", "error")

        return redirect(url_for("admin_dorm.dorm_list"))

    return render_template("admin_dorm_edit.html", dorm=dorm)

# 🗑️ ลบหอพัก
@bp.route("/<int:dorm_id>/delete", methods=["POST"])
def delete_dorm(dorm_id):
    dorm = Dormitory.query.get_or_404(dorm_id)

    try:
        db.session.delete(dorm)
        db.session.commit()
        flash(f"ลบหอพัก {dorm.name} เรียบร้อยแล้ว 🗑️", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"เกิดข้อผิดพลาดในการลบหอพัก: {str(e)}", "error")

    return redirect(url_for("admin_dorm.dorm_list"))

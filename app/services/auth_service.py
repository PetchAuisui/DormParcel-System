from flask import redirect, url_for, flash
from app.models.user_model import User
from app.extensions import db
from app.utils.session_manager import SessionManager
from datetime import datetime

class AuthService:
    def register(
        self, full_name, email, password, role, national_id,
        phone=None, gender=None, date_of_birth=None,
        dorm_id=None, room_id=None
    ):
        # ตรวจสอบความถูกต้องของบัตรประชาชน
        if not national_id.isdecimal() or len(national_id) != 13:
            flash('หมายเลขบัตรประชาชนไม่ถูกต้อง กรุณาลองอีกครั้ง', 'warning')
            return redirect(url_for('auth.register'))

        # ตรวจสอบการซ้ำ
        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้งานแล้ว', 'warning')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(national_id=national_id).first():
            flash('หมายเลขบัตรประชาชนนี้ถูกใช้งานแล้ว', 'warning')
            return redirect(url_for('auth.register'))

        if phone and User.query.filter_by(phone=phone).first():
            flash('หมายเลขโทรศัพท์นี้ถูกใช้งานแล้ว', 'warning')
            return redirect(url_for('auth.register'))

        # แปลงวันเกิด (string → date)
        dob = None
        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                flash('รูปแบบวันเกิดไม่ถูกต้อง (เช่น 2001-12-31)', 'warning')
                return redirect(url_for('auth.register'))

        # สร้างผู้ใช้ใหม่
        new_user = User(
            full_name=full_name,
            national_id=national_id,
            email=email,
            phone=phone,
            gender=gender,
            date_of_birth=dob,
            dorm_id=dorm_id or None,
            room_id=room_id or None,
            role=role
        )

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('auth.login'))

    def login(self, identifier, password):
        # เข้าระบบด้วยอีเมลหรือเบอร์โทร
        if '@' in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(phone=identifier).first()

        if not user or not user.check_password(password):
            flash('อีเมล/เบอร์โทรศัพท์ หรือรหัสผ่านไม่ถูกต้อง', 'danger')
            return redirect(url_for('auth.login'))

        SessionManager.login_user(user)
        flash(f"ยินดีต้อนรับ, {user.full_name}!", 'success')
        return redirect(url_for('main.index'))

    def logout(self):
        SessionManager.logout_user()
        flash('ออกจากระบบเรียบร้อยแล้ว', 'success')
        return redirect(url_for('auth.login'))

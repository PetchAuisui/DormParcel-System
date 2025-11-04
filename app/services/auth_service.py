from flask import Flask,redirect, url_for,flash
from app.models.user_model import User
from app.extensions import db
from app.utils.session_manager import SessionManager

class AuthService:
    def register(self, full_name, email, password, role, national_id, dorm_id=None, room_id=None, phone=None):
        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้งานแล้ว', 'warning')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(national_id=national_id).first():
            flash('หมายเลขบัตรประชาชนนี้ถูกใช้งานแล้ว', 'warning')
            return redirect(url_for('auth.register'))
        new_user = User(
            full_name=full_name,
            email=email,
            national_id=national_id,
            phone=phone,
            dorm_id=dorm_id,
            room_id=room_id,
            role=role
        )

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('auth.login'))
    

    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
            return redirect(url_for('auth.login'))
        
        SessionManager.login_user(user)
        flash(f"ยินดีต้อนรับ, {user.full_name}!", 'success')
        return redirect(url_for('main.index'))
    
    def logout(self):
        SessionManager.logout_user()
        flash('ออกจากระบบเรียบร้อยแล้ว', 'success')
        return redirect(url_for('auth.login'))
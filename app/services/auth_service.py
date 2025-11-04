from flask import Flask,redirect, url_for,flash
from app.models.user_model import User
from app.extensions import db
from app.utils.session_manager import SessionManager

class AuthService:
    def register(self, full_name, email, password, role, room_number=None):
        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้งานแล้ว', 'warning')
            return redirect(url_for('auth.register'))

        if role == "RESIDENT" and not room_number:
            flash('กรุณาระบุหมายเลขห้องสำหรับผู้พักอาศัย', 'warning')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            full_name=full_name,
            email=email,
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
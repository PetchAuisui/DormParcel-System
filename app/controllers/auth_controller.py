from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        national_id = request.form.get('national_id')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        date_of_birth = request.form.get('date_of_birth')
        role = request.form.get('role')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 🔒 ตรวจสอบข้อมูลเบื้องต้น
        if not all([full_name, national_id, email, password, confirm_password, role]):
            flash('กรุณากรอกข้อมูลให้ครบทุกช่อง', 'warning')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('รหัสผ่านทั้งสองช่องไม่ตรงกัน กรุณาลองอีกครั้ง', 'warning')
            return redirect(url_for('auth.register'))

        return auth_service.register(
            full_name=full_name,
            email=email,
            password=password,
            role=role,
            national_id=national_id,
            phone=phone,
            gender=gender,
            date_of_birth=date_of_birth
        )

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        if not identifier or not password:
            flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'warning')
            return redirect(url_for('auth.login'))

        return auth_service.login(identifier, password)

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    return auth_service.logout()

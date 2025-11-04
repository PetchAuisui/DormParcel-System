from flask import Blueprint, request , render_template
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        national_id = request.form.get('national_id')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')


        if password != request.form.get('confirm_password'):
            flash('รหัสผ่านทั้งสองช่องไม่ตรงกัน กรุณาลองอีกครั้ง', 'warning')
            return redirect(url_for('auth.register'))

        return auth_service.register(full_name, email, password, role, national_id, phone=phone)
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        return auth_service.login(email, password)
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    return auth_service.logout()
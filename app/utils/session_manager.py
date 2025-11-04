from flask import session

class SessionManager:
    @staticmethod
    def login_user(user):
        session['user_id'] = user.user_id
        session['user_name'] = user.full_name
        session['role'] = user.role
        session['dorm_id'] = user.dorm_id
        session['room_id'] = user.room_id

    @staticmethod
    def logout_user():
        session.clear()

    @staticmethod
    def is_logged_in():
        if "user_id" in session:
            return {
                "id": session["user_id"],
                "name": session["user_name"],
                "role": session["role"],
                "dorm_id": session.get("dorm_id"),
                "room_id": session.get("room_id")
            }
        return None

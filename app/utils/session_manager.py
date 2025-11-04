from flask import session

class SessionManager:
    @staticmethod
    def login(user):
        session['user_id'] = user.user_id
        session['user_name'] = user.full_name
        session['role'] = user.role

    @staticmethod
    def logout():
        session.clear()

    @staticmethod
    def is_logged_in():
        if "user_id" in session:
            return {
                "id": session["user_id"],
                "name": session["user_name"],
                "role": session["role"]
            }
        return None
from functools import wraps
from flask import abort
from flask_login import current_user

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_role not in ["superadmin"]:
            abort(404)  # Or redirect to an unauthorized page
        return f(*args, **kwargs)
    return decorated_function
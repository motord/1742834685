"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort
from models import Profile

def profile_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        user=users.get_current_user()
        if not user:
            return redirect(users.create_login_url(request.url))
        profile=Profile.query(Profile.user==user).get()
        if not profile:
            profile=Profile(user=user, nickname=user.nickname(), email=user.email())
        profile.put()
        kwargs['profile']=profile
        return func(*args, **kwargs)
    return decorated_view
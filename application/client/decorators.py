"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort
from models import Profile
import logging

def profile_required(func):
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

def ownership_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.is_current_user_admin():
            profile=kwargs['profile']
            key=kwargs['key']
            if key.kind()=='QRCode':
                key=key.get().campaign
            if key not in profile.campaigns:
                abort(401)
        return func(*args, **kwargs)
    return decorated_view
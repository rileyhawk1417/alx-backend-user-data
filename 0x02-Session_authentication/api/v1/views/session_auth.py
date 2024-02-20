#!/usr/bin/env python3

"""
Module that handles the api interface
For managing sessions.
"""
from os import getenv
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def user_login() -> Tuple[str, int]:
    """
    POST /api/v1/auth_session/login
    Return:
        JSON tuple of User object
    """
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({'error': 'password missing'}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404
    if not users or users == []:
        return jsonify({'error': 'no user found for this email'}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(getattr(users[0], 'id'))
            reply = jsonify(user.to_json())
            reply.set_cookie(getenv('SESSION_NAME'), session_id)
            return reply
    return jsonify({'error': 'wrong password'}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def user_logout() -> Tuple[str, int]:
    """
    DELETE /api/v1/auth_session/logout
    Returns:
        Empty tuple
    """
    from api.v1.app import auth
    is_deleted = auth.destroy_session(request)
    if not is_deleted:
        abort(404)
    return jsonify({})

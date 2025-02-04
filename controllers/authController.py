import bcrypt
import jwt
import datetime
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

from models.user import User

db = SQLAlchemy()

class AuthController:
    @staticmethod
    def auth():
        try:
            username = request.get_json()['username']
            password = request.get_json()['password']

            try:
                user = User.query.filter_by(username=username).first()
                if (bcrypt.checkpw(password.encode('utf-8'), bytes(user.password, 'utf-8'))):
                    user_serialize = user.serialize
                    token = jwt.encode(
                        {'user': user_serialize, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, 'Bearer')
                    return jsonify({'user': user_serialize, 'token': token}), 200
                raise
            except:
                return jsonify({'message': 'Email or password is incorrect'}), 401
        except:
            return jsonify({'message': 'The request body required username, password'}), 400

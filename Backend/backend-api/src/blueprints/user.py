import jwt
from flask import request, jsonify, Blueprint, Response
from src.utils.auth_policy import authenticated
from src.dao.user_dao import UserDAO
from src.utils.jwt import generate_token
from src.exceptions import UserWithSameName

user_blueprint = Blueprint('user_blueprint', __name__,  url_prefix='/user')

@user_blueprint.post('/signup')
def signup():
  user = request.json
  try:
    user_doc = UserDAO.get(user['username'])
    if user_doc: raise UserWithSameName
    UserDAO.create(user['username'], user['password'], False)
  except UserWithSameName:
    return jsonify({ 'message': 'UserWithSameName' }), 400
  except Exception as err:
    print('Exception:', err)
    return jsonify({ 'message': 'InvalidRequest' }), 400
  return jsonify({ 'ok': True }), 200

@user_blueprint.post('/signin')
def signin():
  user = request.json
  try:
    is_correct = UserDAO.is_password_correct(user['username'], user['password'])
    if not is_correct: return jsonify({ 'message': 'WrongPass' }), 401
    user_doc = UserDAO.get(user['username'])
    token = generate_token({
      'username': user['username'],
      'is_admin': user_doc['is_admin']
    })
  except Exception as err:
    print('Exception:', err)
    return jsonify({ 'message': 'InvalidRequest' }), 400
  return jsonify({ 'token': token }), 200

@user_blueprint.get('/')
@authenticated
def getUser(user={}):
  try:
    user_doc = UserDAO.get(user['username'])
    del user_doc['pwd_hash']
  except Exception as err:
    print('Exception:', err)
    return jsonify({ 'message': 'InvalidRequest' }), 400
  return jsonify(user_doc), 200


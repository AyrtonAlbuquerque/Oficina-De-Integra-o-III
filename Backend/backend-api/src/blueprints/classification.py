import os
from flask import request, jsonify, Blueprint
from src.utils.auth_policy import authenticated
from src.dao.user_dao import UserDAO
from src.utils.redeem_code import generate_redeem_code
from src.utils.network_interface import classify
from src.dao.classification_dao import ClassificationDAO
from src.config import STORAGE_PATH

classification_blueprint = Blueprint('classification_blueprint', __name__,  url_prefix='/classifications')

@classification_blueprint.post('/request')
def classificationRequest():
    try:
        recycler_id = request.form['recyclerID']
        redeem_code = generate_redeem_code()
        image_path = os.path.join(STORAGE_PATH, redeem_code + '.jpg')
        request.files['file'].save(image_path)
        label = classify(image_path)
        label = label if label != 0 else 6
        classification = {
            'recycler_id': recycler_id,
            'label': label,
            'redeem_code': redeem_code,
            'image_path': image_path
        }
        print('classification', classification)
        ClassificationDAO.create(classification)
    except Exception as err:
        print('Exception:', err)
        return jsonify({ 'message': 'InvalidRequest' }), 400
    return jsonify({'class': label, 'redeem_code': redeem_code})

@classification_blueprint.get('/statistics')
@authenticated
def get_classification_statistics(user={}):
  try:
    statistics = ClassificationDAO.classification_statistics()
  except Exception as err:
    print('Exception:', err)
    return jsonify({ 'message': 'InvalidRequest' }), 400
  return jsonify({ 'statistics': statistics }), 200


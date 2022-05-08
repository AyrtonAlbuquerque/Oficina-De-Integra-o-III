from flask import request, jsonify, Blueprint, Response
from src.utils.auth_policy import authenticated
from src.dao.transaction_dao import TransactionDAO
from src.dao.classification_dao import ClassificationDAO
from src.dao.user_dao import UserDAO
from src.exceptions import InsufficientFunds, InvalidRedeemCode, NotFound
from src.utils.label_to_credits import LABEL_TO_CREDITS


transaction_blueprint = Blueprint('transaction_blueprint', __name__,  url_prefix='/transactions')


@transaction_blueprint.post('/send')
@authenticated
def send_transaction(user={}):
    try:
        transaction = request.json
        if transaction['amount'] <= 0: raise Exception('NegativeAmount')
        if not UserDAO.get(transaction['to_account']): raise NotFound
        TransactionDAO.transact(
            user['username'],
            transaction['to_account'],
            transaction['amount'])
    except InsufficientFunds:
        return jsonify({ 'message': 'InsufficientFunds' }), 400
    except NotFound:
        return jsonify({ 'message': 'NotFound' }), 404
    except Exception as err:
        print('Exception:', err)
        return jsonify({ 'message': 'InvalidRequest' }), 400
    return jsonify({ 'ok': True })


@transaction_blueprint.post('/give_credits')
@authenticated
def give_credits(user={}):
    try:
        classification_data = request.json
        redeem_code = classification_data['redeem_code']
        label = classification_data['label']
        if not ClassificationDAO.classification_with_redeem_code_exists(redeem_code):
          raise InvalidRedeemCode
        ClassificationDAO.redeem_code_from_classification(redeem_code)
        credits_amount = LABEL_TO_CREDITS[str(label)]
        TransactionDAO.give_credits(user['username'], credits_amount)
    except InvalidRedeemCode:
        return jsonify({ 'message': 'InvalidRedeemCode' }), 400
    except Exception as err:
        print('Exception:', err)
        return jsonify({ 'message': 'InvalidRequest' }), 400
    return jsonify({ 'ok': True })


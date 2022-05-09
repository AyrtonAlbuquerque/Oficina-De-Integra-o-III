from flask import Flask, jsonify
from flask_cors import CORS
from src.database import setup
from src.config import PORT
from src.blueprints.user import user_blueprint
from src.blueprints.classification import classification_blueprint
from src.blueprints.transaction import transaction_blueprint

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# setup database
setup()

# enable CORS
CORS(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(classification_blueprint)
app.register_blueprint(transaction_blueprint)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run(port=PORT)
from flask import Flask, current_app, request, jsonify, make_response, Blueprint
import io
import model
import base64
import logging

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

api = Blueprint('api', app, url_prefix='/api/v1')

@api.route('/books', methods=['POST'])
def predict():

    if request.headers['Content-Type'] != 'application/json':
        return jsonify(status_code='415', msg='Unsupported Media Type'), 415

    try:
        data = {}
        data = request.get_json()['data']
    except Exception:
        return jsonify(status_code='400', msg='Bad Request'), 400

    data = base64.b64decode(data)

    image = io.BytesIO(data)
    predictions = model.predict(image)
    current_app.logger.info('Predictions: %s', predictions)

    return jsonify(predictions=predictions)

@api.errorhandler(404)
def not_found(error):
    return jsonify(status_code='404', msg='Not found'), 404

'''
POST api.goodscifi.com/v1/books #return predictions

# better?
POST api.goodscifi.com/v1/books/ #returns book_id
GET api.goodscifi.com/v1/books/<book_id>/predictions #returns predictions
GET api.goodscifi.com/v1/movies/predictions?filter_by=recent
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

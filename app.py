# _*_ coding: utf-8 _*_
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pickle
import model_test
import json
from flask import Response
from functools import wraps
import sys
from flask import make_response

app = Flask(__name__)
api = Api(app)




def as_json(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        res = f(*args, **kwargs)

        res = json.dumps(res, ensure_ascii=False).encode('utf8')

        return Response(res, content_type='application/json; charset=utf-8')

    return decorated_function



class get_ml_data(Resource):
    @as_json
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('objId', type=str)
            args = parser.parse_args()
            objId = args['objId']
            keyword, topic_result = model_test.get_result(objId)
            return {'status': 'success', 'keyword' : keyword, 'topic_result': topic_result}
            # return {'status':200}
        except Exception as e:
            print('error : ',e)
            return {'status': 400, 'message' : e}

api.add_resource(get_ml_data, '/ml')

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':


    model_test.init()
    app.run(host='0.0.0.0', port=5050, debug=True)

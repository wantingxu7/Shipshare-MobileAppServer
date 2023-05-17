import datetime
import json
import os
import traceback

from utils.errors import ServerError
from flask import Response
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError, InvalidTokenError

env = os.getenv('ENV')

# ref: https://stackoverflow.com/questions/67596481/how-to-remove-all-the-oid-and-date-in-a-json-file


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if hasattr(obj, '__str__'):
            return str(obj)

        return super(MyJsonEncoder, self).default(obj)

# ref: https://github.com/LiViz-cc/lvz-backend/blob/main/resources/response_wrapper.py


def response_wrapper(use_converter=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # get response
                response = func(*args, **kwargs)

                if not use_converter:
                    return Response(response, mimetype='application/json', status=200)

                response_json: str
                if type(response) == dict:
                    response_json = json.dumps(response, cls=MyJsonEncoder)

                elif type(response) == list:
                    response_json_list = [x.to_json() for x in response]
                    response_json = '[' + ','.join(response_json_list) + ']'

                else:
                    response_json = response.to_json()

                return Response(response_json, mimetype='application/json', status=200)
            except NoAuthorizationError as e:
                # wrap jwt authorization error
                return {'title': 'Forbidden', 'status': 403, 'detail': 'Cannot access with given authorization.'}, 403
            except ServerError as e:
                # wrap server error with given status and error title, detail
                return {'title': e.title, 'status': e.status, 'detail': e.detail}, e.status
            except InvalidTokenError as e:
                # return no detail if not in development
                detail = '' if env != 'development' else str(e)

                return {'title': 'Token Invalid Error', 'status': 401, 'detail': detail}, 401
            except Exception as e:
                if env == 'development':
                    raise e

                # return no detail if not in development
                detail = '' if env != 'development' else str(e)
                # wrap other exceptions with status 500
                return {'title': 'Internal Server Error', 'status': 500, 'detail': detail}, 500
        return wrapper
    return decorator


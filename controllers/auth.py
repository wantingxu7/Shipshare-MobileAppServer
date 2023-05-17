
from services.user_service import UserService
import utils
from flask import request
from flask_restful import Resource
from utils.errors import InvalidParamError
from utils.response_wrapper import response_wrapper


class SignupResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.user_service = UserService()

    @response_wrapper()
    def post(self):
        # get request body dict
        body = request.get_json()

        # Unpack body
        email = body.get('email', None)
        password = body.get('password', None)

        return self.user_service.signUp(email, password)


class LoginResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.user_service = UserService()

    @response_wrapper()
    def post(self):
        # get request body dict
        body = request.get_json()

        email = body.get('email', None)
        password = body.get('password', None)
        username = body.get('username')

        if email is None and username is None:
            raise InvalidParamError('Please provide email or username.')

        if email is not None and username is not None:
            raise InvalidParamError('Please provide either username or email.')

        return self.user_service.login(email, password, username)

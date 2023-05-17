
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from services.user_service import UserService
from utils import response_wrapper
from utils.errors import InvalidParamError

class UserPasswordResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.user_service = UserService()

    @response_wrapper()
    @jwt_required()
    def post(self, id):
        # get request body dict
        body = request.get_json()

        # check authorization
        jwt_id = get_jwt_identity()

        # query project via id
        new_password = body.get('new_password', None)

        return self.user_service.change_password(id, jwt_id, new_password)


class UserResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.user_service = UserService()

    @response_wrapper()
    @jwt_required(optional=True)
    def get(self, id):
        jwt_id = get_jwt_identity()

        return self.user_service.get_user_by_id(id, jwt_id)


class UserAvatarResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.user_service = UserService()

    @response_wrapper()
    @jwt_required()
    def post(self, id):
        # get request body dict
        body = request.get_json()

        # check authorization
        jwt_id = get_jwt_identity()

        # query project via id
        avatar = body.get('avatar', None)

        # check if avatar is provided
        if avatar is None:
            raise InvalidParamError('Please provide avatar.')

        return self.user_service.change_avatar(jwt_id, avatar)
    

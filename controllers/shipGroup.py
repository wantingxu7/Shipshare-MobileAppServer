
from services.shipGroup_service import ShipGroupService
import utils
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from utils import response_wrapper


class ShipGroupsResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.ship_group_service = ShipGroupService()

    @response_wrapper()
    @jwt_required(optional=True)
    def get(self):
        args = request.args
        jwt_id = get_jwt_identity()
        email = args.get('email')

        return self.ship_group_service.get_ship_groups_by_user_email(email, jwt_id)

    @response_wrapper()
    @jwt_required()
    def post(self):
        # get request body dict
        body = request.get_json()

        # get authorization
        jwt_id = get_jwt_identity()

        return self.ship_group_service.create_ship_group(body, jwt_id)


class ShipGroupResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.ship_group_service = ShipGroupService()

    @response_wrapper()
    @jwt_required(optional=True)
    def get(self, id):
        user_id = get_jwt_identity()

        return self.ship_group_service.get_ship_group_by_id(id, user_id)

    @response_wrapper()
    @jwt_required()
    def put(self, id):
        # get request body dict
        body = request.get_json()

        # get authorization
        jwt_id = get_jwt_identity()

        return self.ship_group_service.edit_ship_group(id, body, jwt_id)

    @response_wrapper()
    @jwt_required()
    def delete(self, id):
        # get authorization
        jwt_id = get_jwt_identity()

        return self.ship_group_service.delete_ship_group(id, jwt_id)


class ShipGroupMembersResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.ship_group_service = ShipGroupService()

    @response_wrapper()
    @jwt_required()
    def get(self, email):
        # get authorization
        jwt_id = get_jwt_identity()

        # get ship_groups whose members include email
        return self.ship_group_service.get_ship_groups_whose_members_include(email, jwt_id)


class ShipGroupAddMemberResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.ship_group_service = ShipGroupService()

    @response_wrapper()
    @jwt_required()
    def post(self, shipGroupId):
        # get authorization
        jwt_id = get_jwt_identity()

        return self.ship_group_service.add_a_user_to_ship_group_members(shipGroupId, jwt_id)


class ShipGroupRemoveMemberResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.ship_group_service = ShipGroupService()

    @response_wrapper()
    @jwt_required()
    def post(self, shipGroupId):
        # get authorization
        jwt_id = get_jwt_identity()

        return self.ship_group_service.remove_a_user_from_ship_group_members(shipGroupId, jwt_id)
    

import utils
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from services.parcel_service import ParcelService
from utils import response_wrapper


class ParcelsResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.parcel_service = ParcelService()

    @response_wrapper()
    @jwt_required(optional=True)
    def get(self):
        args = request.args
        jwt_id = get_jwt_identity()
        email = args.get('email')
        ship_group_id = args.get('shipGroup')
        if email is not None:
            return self.parcel_service.get_parcels_by_user_email(email, jwt_id)

        if ship_group_id is not None:
            return self.parcel_service.get_parcels_by_shipGroup(ship_group_id, jwt_id)

        return {}

    @response_wrapper()
    @jwt_required()
    def post(self):
        # get request body dict
        body = request.get_json()

        # get authorization
        jwt_id = get_jwt_identity()

        return self.parcel_service.create_parcel(body, jwt_id)


class ParcelResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.parcel_service = ParcelService()

    @response_wrapper()
    @jwt_required(optional=True)
    def get(self, id):
        user_id = get_jwt_identity()

        return self.parcel_service.get_parcel_by_id(id, user_id)

    @response_wrapper()
    @jwt_required()
    def put(self, id):
        # get request body dict
        body = request.get_json()

        # get authorization
        jwt_id = get_jwt_identity()

        return self.parcel_service.edit_parcel(id, body, jwt_id)

    @response_wrapper()
    @jwt_required()
    def delete(self, id):
        # get authorization
        jwt_id = get_jwt_identity()

        return self.parcel_service.delete_parcel(id, jwt_id)

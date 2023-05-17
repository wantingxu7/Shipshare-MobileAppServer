
import datetime
import json
from dao import ParcelDao
from dao.shipGroup_dao import ShipGroupDao
from dao.user_dao import UserDao

from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)
from flask_jwt_extended import create_access_token
from models.Parcel import Parcel
import utils


class ParcelService():
    def __init__(self) -> None:
        self.parcel_dao = ParcelDao()
        self.user_dao = UserDao()
        self.ship_group_dao = ShipGroupDao()

    def get_parcels_by_user_email(self, email, jwt_id):
        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        # query parcels via user id
        parcels = self.parcel_dao.query_parcels(user=email)

        return list(parcels)
    
    def get_parcels_by_shipGroup(self, ship_group_id, jwt_id):
        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        # query parcels via shipGroup id
        parcels = self.parcel_dao.query_parcels(shipGroup=ship_group_id)

        return list(parcels)
    
    def get_parcel_by_id(self, id, jwt_id) -> Parcel:
        # query parcel via id
        parcel = self.parcel_dao.get_parcel_by_id(id)

        return parcel

    def create_parcel(self,
                      body: dict,
                      jwt_id: str) -> Parcel:

        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        if body.get('id') is not None:
            return self.edit_parcel(body['id'], body, jwt_id)

        # construct new parcel object
        parcel = Parcel(**body)

        # set time
        curr_time = datetime.datetime.utcnow
        parcel.created = curr_time
        parcel.modified = curr_time

        # set created by
        parcel.user = user.email

        # change `shipGroup` to reference
        shipGroup = body.get('shipGroup')
        if shipGroup is not None:
            if shipGroup == "":
                parcel['shipGroup'] = None
            else:
                parcel['shipGroup'] = self.ship_group_dao.get_ship_group_by_id(
                    shipGroup)

        # save new parcel
        self.parcel_dao.save(parcel)

        return parcel

    def edit_parcel(self, id, body: dict, jwt_id) -> Parcel:
        # avoid id and user being modified
        body.pop('id', None)
        body.pop('user', None)

        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        # query parcel via id
        parcel = self.parcel_dao.get_parcel_by_id(id)

        # list of shipGroup whose totalWeight should be updated
        ship_groups_to_update = []

        if parcel.shipGroup is not None:
            ship_groups_to_update.append(parcel.shipGroup)

        if parcel.user != user.email:
            raise ForbiddenError("You can only query your own parcels")

        # set time
        curr_time = datetime.datetime.utcnow
        body['modified'] = curr_time

        # change `shipGroup` to reference
        shipGroup = body.get('shipGroup')
        if shipGroup is not None:
            if shipGroup == "":
                body['shipGroup'] = None
            else:
                new_ship_group = self.ship_group_dao.get_ship_group_by_id(
                    shipGroup)
                body['shipGroup'] = new_ship_group
                ship_groups_to_update.append(new_ship_group)

        # update parcel
        self.parcel_dao.modify(parcel, body)

        # update total weight
        for ship_group in ship_groups_to_update:
            self.ship_group_dao._add_total_weight(ship_group)

        return parcel

    def delete_parcel(self, id: str, jwt_id: str) -> dict:
        # check auth
        user = self.user_dao.get_user_by_id(jwt_id)

        # query parcel via id
        parcel = self.parcel_dao.get_parcel_by_id(id)

        # check authorization
        if parcel.user != user.email:
            raise ForbiddenError("You can only query your own parcels")

        # delete parcel
        self.parcel_dao.delete(parcel)

        return {}

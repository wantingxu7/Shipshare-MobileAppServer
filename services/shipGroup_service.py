
import datetime
import json
from dao import ShipGroupDao
from dao.user_dao import UserDao
from models.Parcel import Parcel

from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)
from flask_jwt_extended import create_access_token
from models.ShipGroup import ShipGroup
import utils


class ShipGroupService():
    def __init__(self) -> None:
        self.ship_group_dao = ShipGroupDao()
        self.user_dao = UserDao()

    def _add_total_weight(self, ship_group: ShipGroup):
        # get all parcels in this ship_group
        parcels = Parcel.objects(shipGroup=ship_group)

        # calculate total weight
        total_weight = sum(parcel.weight for parcel in parcels if parcel.weight is not None)

        # update total weight
        ship_group.totalWeight = total_weight

        # save again
        self.ship_group_dao.save(ship_group)

    def get_ship_groups_by_user_email(self, email, jwt_id):
        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        # query ship_groups via user id
        ship_groups = self.ship_group_dao.query_ship_groups(user=email)

        for ship_group in ship_groups:
            # update total weight
            self.ship_group_dao._add_total_weight(ship_group)

        return list(ship_groups)

    def get_ship_group_by_id(self, id, jwt_id) -> ShipGroup:
        # query ship_group via id
        ship_group = self.ship_group_dao.get_ship_group_by_id(id)

        # update total weight
        self._add_total_weight(ship_group)

        return ship_group

    def create_ship_group(self,
                          body: dict,
                          jwt_id: str) -> ShipGroup:
        body.pop('totalWeight', None)

        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        if body.get('id') is not None:
            return self.edit_ship_group(body['id'], body, jwt_id)

        # construct new ship_group object
        ship_group = ShipGroup(**body)

        # set time
        curr_time = datetime.datetime.utcnow
        ship_group.created = curr_time
        ship_group.modified = curr_time

        # set created by
        ship_group.user = user.email

        # save new ship_group
        self.ship_group_dao.save(ship_group)

        # update total weight
        self._add_total_weight(ship_group)

        # save again
        self.ship_group_dao.save(ship_group)

        return ship_group
    
    def edit_ship_group(self, id, body: dict, jwt_id) -> ShipGroup:
        # avoid id and user being modified
        body.pop('id', None)
        body.pop('user', None)

        body.pop('totalWeight', None)

        # get jwt user
        user = self.user_dao.get_user_by_id(jwt_id)

        # query ship_group via id
        ship_group = self.ship_group_dao.get_ship_group_by_id(id)

        if ship_group.user != user.email:
            raise ForbiddenError("You can only query your own ship groups")

        # set time
        curr_time = datetime.datetime.utcnow
        body['modified'] = curr_time

        # update ship_group
        self.ship_group_dao.modify(ship_group, body)

        # update total weight
        self._add_total_weight(ship_group)

        print("ship_group", ship_group)

        # save again
        self.ship_group_dao.save(ship_group)

        return ship_group

    def delete_ship_group(self, id: str, jwt_id: str) -> dict:
        # check auth
        user = self.user_dao.get_user_by_id(jwt_id)

        # query ship_group via id
        ship_group = self.ship_group_dao.get_ship_group_by_id(id)

        # check authorization
        if ship_group.user != user.email:
            raise ForbiddenError("You can only query your own ship groups")

        # delete ship_group
        self.ship_group_dao.delete(ship_group)

        return {}

    def get_ship_groups_whose_members_include(self, email: str, jwt_id: str) -> list:
        # check auth
        user = self.user_dao.get_user_by_id(jwt_id)

        # check authorization
        if user.email != email:
            raise ForbiddenError("You can only query your own ship groups")

        # query ship_groups whose members include email
        ship_groups = self.ship_group_dao.query_ship_groups(
            members__contains=email)

        return list(ship_groups)

    def add_a_user_to_ship_group_members(self, ship_group_id: str, jwt_id: str) -> ShipGroup:
        # check auth
        user = self.user_dao.get_user_by_id(jwt_id)

        # query ship_group via id
        ship_group = self.ship_group_dao.get_ship_group_by_id(ship_group_id)

        # check if ship_group.members is None
        if ship_group.members is None:
            ship_group.members = []

        # check authorization
        if user.email in ship_group.members:
            raise ForbiddenError("You have already joined this ship group")

        # add member to ship_group
        ship_group.members.append(user.email)

        # update total weight
        self._add_total_weight(ship_group)

        # save ship_group
        self.ship_group_dao.save(ship_group)

        return ship_group

    def remove_a_user_from_ship_group_members(self, ship_group_id: str, jwt_id: str) -> ShipGroup:
        # check auth
        user = self.user_dao.get_user_by_id(jwt_id)

        # query ship_group via id
        ship_group = self.ship_group_dao.get_ship_group_by_id(ship_group_id)

        # check authorization
        if user.email not in ship_group.members:
            raise ForbiddenError("You have not joined this ship group")

        # remove member from ship_group
        ship_group.members.remove(user.email)

        # update total weight
        self._add_total_weight(ship_group)

        # save ship_group
        self.ship_group_dao.save(ship_group)

        return ship_group

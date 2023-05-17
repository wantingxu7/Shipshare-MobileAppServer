
import datetime
import json
from dao import UserDao
from dao.parcel_dao import ParcelDao
from dao.shipGroup_dao import ShipGroupDao

from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)
from flask_jwt_extended import create_access_token
from models.User import User
import utils


class UserService():
    def __init__(self) -> None:
        self.user_dao = UserDao()
        self.parcel_dao = ParcelDao()
        self.ship_group_dao = ShipGroupDao()

    def _count_parcels(self, user):
        # count parcels
        return self.parcel_dao.count_parcels_with_email(user.email)

    def _count_shipments(self, user):
        # count shipments
        return self.ship_group_dao.count_shipments_with_email(user.email)

    def _add_counts_in_user(self, user) -> None:
        # add counts in user
        user.numberParcels = self._count_parcels(user)
        user.numberShipments = self._count_shipments(user)

    def get_user_by_id(self, id, jwt_id) -> User:
        # query user via id
        user = self.user_dao.get_user_by_id(id)

        # user can only get their own info
        if jwt_id != str(user.id):
            print("jwt_id:, user.id:", jwt_id, user.id)
            raise ForbiddenError("You can only get your own info.")
        
        # add counts in user
        self._add_counts_in_user(user)

        return user

    def signUp(self, email: str, password: str, *args, **kwargs):

        # Pack body
        body = {'email': email, 'password': password}

        # construct new user object
        user = User(**body)

        # set time
        curr_time = utils.get_utcnow()
        user.created = curr_time
        user.modified = curr_time

        # hash passord
        # must manually call this function before save
        self.user_dao.hash_password(user)

        # save new user
        self.user_dao.save(user)

        # create access token
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id), expires_delta=expires)

        # return desensitized created user
        self.user_dao.desensitize(user)

        return {'token': access_token, 'user': json.loads(user.to_json())}

    def login(self, email: str, password: str, username: str):
        # query user
        if email is not None:
            user = self.user_dao.get_user_by_email_with_password(email)
        else:
            raise InvalidParamError('Please provide email.')

        # check password
        self.user_dao.assert_password_match(user, password)

        # create access token
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id), expires_delta=expires)

        # return desensitized created user
        self.user_dao.desensitize(user)

        # add counts in user
        self._add_counts_in_user(user)

        return {'token': access_token, 'user': json.loads(user.to_json())}

    def change_password(self, id, jwt_id, new_password):
        # user can only change their own password
        if id != jwt_id:
            raise ForbiddenError("You can only query your own password.")

        # get user from database
        user = self.user_dao.get_user_by_id_with_password(id)

        modifing_dict = {}

        modifing_dict['password'] = self.user_dao.get_password_hash(
            new_password)
        modifing_dict['modified'] = datetime.datetime.utcnow

        # update project
        self.user_dao.modify(user, modifing_dict)

        self.user_dao.desensitize(user)
        return user


    def change_avatar(self, jwt_id, image_url):
        # get user from database
        user = self.user_dao.get_user_by_id(jwt_id)

        modifing_dict = {}

        modifing_dict['avatar'] = image_url
        modifing_dict['modified'] = datetime.datetime.utcnow

        # update project
        self.user_dao.modify(user, modifing_dict)

        self.user_dao.desensitize(user)
        return user
    
    

from flask_restful import Api
from controllers.auth import LoginResource, SignupResource
from controllers.parcel import ParcelResource, ParcelsResource

from controllers.root import RootResource
from controllers.shipGroup import ShipGroupAddMemberResource, ShipGroupMembersResource, ShipGroupRemoveMemberResource, ShipGroupResource, ShipGroupsResource
from controllers.user import UserPasswordResource, UserResource, UserAvatarResource
from controllers.image_resource import ImagesResource


def init_routes(api: Api):
    api.add_resource(RootResource, '/')

    api.add_resource(SignupResource, '/signup')
    api.add_resource(LoginResource, '/login')

    api.add_resource(ParcelResource, '/parcel/<id>')
    api.add_resource(ParcelsResource, '/parcels')

    api.add_resource(UserPasswordResource, '/user/<id>/password')
    api.add_resource(UserResource, '/user/<id>')
    api.add_resource(UserAvatarResource, '/user/<id>/avatar')

    api.add_resource(ShipGroupResource, '/ship_group/<id>')
    api.add_resource(ShipGroupsResource, '/ship_groups')
    api.add_resource(ShipGroupMembersResource, '/ship_groups/members/<email>')

    api.add_resource(ShipGroupAddMemberResource, '/ship_group/<shipGroupId>/joinGroup')
    api.add_resource(ShipGroupRemoveMemberResource, '/ship_group/<shipGroupId>/leaveGroup')
    
    api.add_resource(ImagesResource, '/images')

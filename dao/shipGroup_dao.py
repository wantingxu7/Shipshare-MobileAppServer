
# from mongoengine import Count, Lookup, Match, Unwind
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from models.Parcel import Parcel

from models.ShipGroup import ShipGroup
from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)


class ShipGroupDao:
    def save(self, ship_group: ShipGroup, *args, **kwargs) -> None:
        try:
            ship_group.save(*args, **kwargs)
        except ValidationError as e:
            raise InvalidParamError(e.message)
        except NotUniqueError:
            raise EmailAlreadyExistsError(ship_group.email)

    def modify(self, ship_group: ShipGroup, modifing_dict: dict) -> None:
        try:
            ship_group.modify(**modifing_dict)
        except ValidationError as e:
            raise InvalidParamError(e.message)
        except LookupError as e:
            raise InvalidParamError(e.message)

    def get_ship_group_by_id(self, id: str) -> ShipGroup:

        try:
            ship_group = ShipGroup.objects.get(id=id)
        except DoesNotExist:
            raise NotFoundError('ship_group', 'id={}'.format(id))

        return ship_group

    def query_ship_groups(self, **kwargs) -> ShipGroup:
        try:
            ship_groups = ShipGroup.objects(**kwargs)
        except DoesNotExist:
            raise NotFoundError('ship_group', 'id={}'.format(id))

        return ship_groups

    def count_shipments_with_email(self, email: str) -> int:
        pipeline = [
            {"$match": {"members": email}},
            {"$count": "total"}
        ]

        result = ShipGroup.objects.aggregate(pipeline)
        count = next(result, {'total': 0})['total']

        return count

    def delete(self, ship_group: ShipGroup) -> None:
        try:
            ship_group.delete()
        except DoesNotExist:
            raise NotFoundError('ship_group', 'id={}'.format(ship_group.id))
        except Exception as e:
            raise ForbiddenError(e.message)

    def _add_total_weight(self, ship_group: ShipGroup):
        # get all parcels in this ship_group
        parcels = Parcel.objects(shipGroup=ship_group)

        # calculate total weight
        total_weight = sum(parcel.weight for parcel in parcels if parcel.weight is not None)

        # update total weight
        ship_group.totalWeight = total_weight
        
        # save again
        self.save(ship_group)

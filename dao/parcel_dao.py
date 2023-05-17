
from flask_bcrypt import check_password_hash, generate_password_hash
from models.Parcel import Parcel
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)


class ParcelDao:
    def save(self, parcel: Parcel, *args, **kwargs) -> None:
        try:
            parcel.save(*args, **kwargs)
        except ValidationError as e:
            raise InvalidParamError(e.message)
        except NotUniqueError:
            raise EmailAlreadyExistsError(parcel.email)

    def modify(self, parcel: Parcel, modifing_dict: dict) -> None:
        try:
            parcel.modify(**modifing_dict)
        except ValidationError as e:
            raise InvalidParamError(e.message)
        except LookupError as e:
            raise InvalidParamError(e.message)

    def get_parcel_by_id(self, id: str) -> Parcel:

        try:
            parcel = Parcel.objects.get(id=id)
        except DoesNotExist:
            raise NotFoundError('parcel', 'id={}'.format(id))

        return parcel
    
    def query_parcels(self, **kwargs) -> Parcel:
        try:
            parcels = Parcel.objects(**kwargs)
        except DoesNotExist:
            raise NotFoundError('parcel', 'id={}'.format(id))

        return parcels
    
    def count_parcels_with_email(self, email: str) -> int:
        pipeline = [
            {"$match": {"user": email}},
            {"$count": "total"}
        ]

        result = Parcel.objects.aggregate(pipeline)
        count = next(result, {'total': 0})['total']

        return count
    
    def delete(self, parcel: Parcel) -> None:
        try:
            parcel.delete()
        except DoesNotExist:
            raise NotFoundError('parcel', 'id={}'.format(parcel.id))
        except Exception as e:
            raise ForbiddenError(e.message)
        

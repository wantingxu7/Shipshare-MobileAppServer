
import datetime

import bson
from database import db
from mongoengine.fields import (DateTimeField, EmailField, ListField, IntField,
                                ReferenceField, StringField, FileField, URLField)

from mongoengine import EmbeddedDocumentField

from models.Address import Address


class User(db.Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=60, max_length=60)
    created = DateTimeField(required=True)
    modified = DateTimeField(required=True)
    location = EmbeddedDocumentField(Address)
    avatar = URLField()
    numberShipments = IntField(min_value=0)
    numberParcels = IntField(min_value=0)

    # override
    # inspired by: https://stackoverflow.com/questions/18574358/mongoengine-to-json-does-conver-referencefield-as-oids
    def to_json(self):
        data = self.to_mongo()

        for key in data:
            if isinstance(data[key], datetime.datetime):
                data[key] = data[key].isoformat()

            if isinstance(data[key], bson.objectid.ObjectId):
                data[key] = str(data[key])

            if key == 'deliverty_status':
                deliverty_status = data[key]
                for i in range(len(deliverty_status)):
                    for k in deliverty_status[i]:
                        if isinstance(deliverty_status[i][k], datetime.datetime):
                            deliverty_status[i][k] = deliverty_status[i][k].isoformat(
                            )

            if key == '_id':
                data['id'] = data['_id']
                del data['_id']

        return bson.json_util.dumps(data)

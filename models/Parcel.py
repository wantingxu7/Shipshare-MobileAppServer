
import json
import datetime
import bson
from database import db
from mongoengine.fields import (DateTimeField, EmailField, ListField, BooleanField,
                                ReferenceField, StringField, FileField, IntField, URLField, FloatField)

from mongoengine import EmbeddedDocumentField, EmbeddedDocument

from models.Address import Address


class DeliveryStatus(EmbeddedDocument):
    statusTime = DateTimeField(required=True)
    description = StringField(required=True)


class Parcel(db.Document):
    name = StringField(required=True)
    trackingNumber = StringField(required=True)
    courier = StringField(required=True)
    location = EmbeddedDocumentField(Address)
    shipGroup = ReferenceField('ShipGroup')
    user = EmailField(required=True)
    picture = URLField()
    isShipped = BooleanField(required=True, default=False)
    isWeighted = BooleanField(required=True, default=False)
    weight = FloatField(min_value=0)

    created = DateTimeField(required=True)
    modified = DateTimeField(required=True)

    # override
    # inspired by: https://stackoverflow.com/questions/18574358/mongoengine-to-json-does-conver-referencefield-as-oids

    def to_json(self):
        data = self.to_mongo()

        for key in data:
            if isinstance(data[key], datetime.datetime):
                data[key] = data[key].isoformat()

            elif isinstance(data[key], bson.objectid.ObjectId):
                data[key] = str(data[key])

            if key == 'delivertyStatus':
                deliverty_status = data[key]
                for i in range(len(deliverty_status)):
                    for k in deliverty_status[i]:
                        if isinstance(deliverty_status[i][k], datetime.datetime):
                            deliverty_status[i][k] = deliverty_status[i][k].isoformat(
                            )

        if '_id' in data:
            data['id'] = data['_id']
            del data['_id']

        return bson.json_util.dumps(data)

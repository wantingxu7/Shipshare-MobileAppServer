
import datetime
import bson
from mongoengine import EmbeddedDocument, EmbeddedDocumentField
from mongoengine.fields import (BooleanField, DateTimeField, EmailField,
                                FileField, IntField, ListField, ReferenceField,
                                StringField, FloatField)

from database import db
from models.Address import Address


class ShipGroup(db.Document):
    name = StringField(required=True)
    shipRoute = StringField(required=True)
    shipEndDate = DateTimeField(required=True)
    pickupLocation = EmbeddedDocumentField(Address)
    user = EmailField(required=True)
    phaseNumber = IntField()
    trackingNumber = StringField()
    courier = StringField(required=True)
    members = ListField(EmailField(required=True), default=[])
    phoneNumber = StringField()

    # auto-generated and saved
    created = DateTimeField(required=True)
    modified = DateTimeField(required=True)

    # auto-generated but not saved
    totalWeight = FloatField()

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

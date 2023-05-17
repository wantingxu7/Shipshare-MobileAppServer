
from database import db
from mongoengine.fields import (DateTimeField, EmailField, ListField,
                                ReferenceField, StringField, BooleanField, FloatField)
from mongoengine import EmbeddedDocument


class Address(EmbeddedDocument):
    name = StringField(required=True)
    address = StringField(required=True)
    notes = StringField(default="")
    geoLatitude = FloatField()
    geoLongitude = FloatField()
    shortAddress = StringField()
    
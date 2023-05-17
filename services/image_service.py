
import datetime
import json
import os
from dao import ShipGroupDao
from dao.user_dao import UserDao

from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)
from flask_jwt_extended import create_access_token
from models.ShipGroup import ShipGroup
import utils
from utils.response_wrapper import response_wrapper
import cloudinary.uploader
import random
import uuid


class ImageService():
    def __init__(self) -> None:
        pass


    def upload_image(self, file, jwt_id):
        # get random name
        random_name = uuid.uuid4().hex

        # Upload the image.
        # Set the asset's public ID and allow overwriting the asset with new versions

        cloudinary.uploader.upload(
            file, public_id=random_name, unique_filename=False, overwrite=True)

        # Build the URL for the image and save it in the variable 'srcURL'
        srcURL = cloudinary.CloudinaryImage(random_name).build_url()

        print(srcURL)

        return {"imageURL": srcURL}

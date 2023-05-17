
from services.image_service import ImageService
import utils
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from utils import response_wrapper


class ImagesResource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.image_service = ImageService()

    @response_wrapper()
    @jwt_required()
    def post(self):
        # get authorization
        jwt_id = get_jwt_identity()

        # get file upload from http request
        file = request.files['file']

        return self.image_service.upload_image(file, jwt_id)

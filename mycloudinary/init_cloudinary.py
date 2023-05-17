import cloudinary
import os


def init_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET'),
        secure=True
    )

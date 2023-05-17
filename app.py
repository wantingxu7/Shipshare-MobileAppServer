import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from mycloudinary.init_cloudinary import init_cloudinary

from controllers.routers import init_routes
from database import init_database
from services.image_service import ImageService

load_dotenv()

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_HOST_URL')
}

print("MONGODB_HOST_URL: ", os.getenv('MONGODB_HOST_URL'))

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

init_database(app)
init_routes(api)
init_cloudinary()

if __name__ == '__main__':
    # load start config
    env = os.getenv('ENV')
    port = int(os.getenv('PORT'))

    # start server
    if env == 'development':
        app.run(debug=True, host="0.0.0.0", port=port)
    elif env == 'production':
        from waitress import serve
        serve(app, host="0.0.0.0", port=port)
    else:
        raise RuntimeError('Fail to start server with ENV=%s!' % env)

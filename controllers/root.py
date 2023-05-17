from flask_restful import Resource

class RootResource(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
        return 'hello world'

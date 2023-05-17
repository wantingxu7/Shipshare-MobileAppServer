
from flask_bcrypt import check_password_hash, generate_password_hash
from models.User import User
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from utils import (EmailAlreadyExistsError, ForbiddenError, InvalidParamError,
                   NotFoundError, NotMutableError, UnauthorizedError)


class UserDao:
    def save(self, user: User, *args, **kwargs) -> None:
        try:
            user.save(*args, **kwargs)
        except ValidationError as e:
            raise InvalidParamError(e.message)
        except NotUniqueError:
            raise EmailAlreadyExistsError(user.email)

    def modify(self, user: User, modifing_dict: dict) -> None:
        # update project
        try:
            user.modify(**modifing_dict)
        except ValidationError as e:
            raise InvalidParamError(e.message)
        except LookupError as e:
            raise InvalidParamError(e.message)

    def get_user_by_id_with_password(self, id: str) -> User:
        try:
            user = User.objects.get(id=id)
        except DoesNotExist:
            raise NotFoundError('user', 'id={}'.format(id))

        return user

    def get_user_by_email_with_password(self, email: str) -> User:
        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            raise UnauthorizedError()
        return user

    def get_user_by_id_with_password(self, id: str) -> User:
        # query user via id
        try:
            user = User.objects.get(id=id)
        except DoesNotExist:
            raise NotFoundError('user', 'id={}'.format(id))

        return user

    def get_user_by_id(self, id: str) -> User:
        user = self.get_user_by_id_with_password(id)

        self.desensitize(user)
        return user
    
    def desensitize(self, user: User):
        if hasattr(user, 'password'):
            del user.password

    def hash_password(self, user: User):
        if not user:
            raise InvalidParamError('User for hashing password cannot be null')
        if not hasattr(user, 'password'):
            raise InvalidParamError(
                'desentitized user has no password attributes')

        user.password = generate_password_hash(user.password).decode('utf8')

    def check_password(self, user: User, password):
        try:
            if user.password == None:
                raise InvalidParamError('desensitized user has no passwords')
        except DoesNotExist as e:
            raise InvalidParamError('desensitized user has no passwords')

        return check_password_hash(user.password, password)

    def assert_password_match(self, user: User, password):
        if not self.check_password(user, password):
            raise ForbiddenError("Password is wrong.")
        
    def get_password_hash(self, password: str) -> str:
        return generate_password_hash(password).decode('utf8')
    
    def get_user_by_email(self, email: str) -> User:
        try:
            user = User.objects.get(email=email)
        except DoesNotExist:
            raise NotFoundError('user', 'email={}'.format(email))

        self.desensitize(user)
        return user
    
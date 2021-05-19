from flask_restful import Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    fresh_jwt_required
)
import traceback

from models.user import UserModel
from schemas.user import UserSchema
from models.confirmation import ConfirmationModel
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from libs.strings import gettext

user_schema = UserSchema()


class UserRegister(Resource):
    """
    Register user - POST: /user/register
    """
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, 400

        try:
            user.password = generate_password_hash(user.password, "sha256")
            user.save_to_db()

            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()

        #    user.send_confirmation_email()
            return {"message": gettext("user_registered")}, 201
        #except MailGunException as e:
        #    user.delete_from_db()  # rollback
        #    return {"message": str(e)}, 500
            
        except:  # failed to save user to db
            traceback.print_exc()
            user.delete_from_db()  # rollback
            return {"message": gettext("user_error_creating")}, 500


class User(Resource):
    """
    Get user by email - GET: /user/<str:email>

    Update user by email - PUT: /user/<str:email>

    Delete user by email - DELETE: /user/<str:email>
    """
    @classmethod
    @jwt_required
    def get(cls, email: str):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return user_schema.dump(user), 200

    @classmethod
    @fresh_jwt_required
    def put(cls, email: str):
        user_json = request.get_json()

        user = UserModel.find_by_email(email)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        
        user = user_schema.load(user_json, partial=("email","password",))

        user.save_to_db()

        return user_schema.dump(user), 200

    @classmethod
    @fresh_jwt_required
    def delete(cls, email: str):
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    """
    User Login - POST: /user/login
    """
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("name",))

        user = UserModel.find_by_email(user_data.email)

        if user and check_password_hash(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(user.id, fresh=True, expires_delta=False)
                refresh_token = create_refresh_token(user.id)
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
            return {"message": gettext("user_not_confirmed").format(user.email)}, 400

        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    """
    User Logout - POST: /user/logout
    """
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "user_logged_out"}, 200


class TokenRefresh(Resource):
    """
    New "access_token" Generator - POST: /user/refresh
    """
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class SetPassword(Resource):
    @classmethod
    @fresh_jwt_required
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_email(user_data.email)

        if not user:
            return {"message": gettext("user_not_found")}, 400

        user.password = generate_password_hash(user_data.password, "sha256")
        user.save_to_db()

        return {"message": gettext("user_password_updated")}, 201

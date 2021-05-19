from flask import request, url_for, g
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
from oa import google

user_schema = UserSchema()


class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        return google.authorize(callback=url_for("google.authorize", _external=True))


# Get authorization
# Create user
# Create access token
# Return JWT
class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = google.authorized_response()
        if resp is None or resp.get('access_token') is None:
            error_response = {
                "error": request.args['error_reason'],
                "error_description": request.args['error_description']
            }
            return error_response

        g.access_token = resp['access_token']
        google_user = google.get('userinfo')  # this uses the access_token from the tokengetter function
        google_user_email = google_user.data["email"]
        google_user_name = google_user.data["name"]
        google_user_picture = google_user.data["picture"]
        
        user = UserModel.find_by_email(google_user_email)

        if not user:
            user = UserModel(email=google_user_email, password=None, name=google_user_name, avatar=google_user_picture)
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.confirmed = True
            confirmation.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)  
        
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

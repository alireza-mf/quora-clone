import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv(".env")

from db import db
from ma import ma
from oa import oauth
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout, SetPassword
from resources.google_login import GoogleLogin, GoogleAuthorize
from resources.answer import CreateAnswer, Answer, ListAnswer
from resources.question import Question, CreateListQuestion
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import UploadAvatar, Avatar, Image
from libs.image_helper import IMAGE_SET


app = Flask(__name__, static_folder = "./frontend/dist/", static_url_path='/') # serve the built frontend
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.secret_key = os.environ.get(
    "APP_SECRET_KEY"
)  # could do app.config['JWT_SECRET_KEY'] if we prefer
app.config["UPLOADED_IMAGES_DEST"] = os.path.join("static", "images")
patch_request_class(app, 4 * 1024 * 1024)  # restrict max upload image size to 4MB
configure_uploads(app, IMAGE_SET)
api = Api(app)
CORS(app) # , resources={r'/*': {'origins': '*'}}

db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/user/register")
api.add_resource(User, "/user/<string:email>")
api.add_resource(UserLogin, "/user/login")
api.add_resource(TokenRefresh, "/user/refresh")
api.add_resource(UserLogout, "/user/logout")
api.add_resource(GoogleLogin, "/login/google")
api.add_resource(GoogleAuthorize, "/login/google/authorized", endpoint="google.authorize")

api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(UploadAvatar, "/upload/avatar")
api.add_resource(Avatar, "/user/avatar/<int:user_id>")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(SetPassword, "/user/password")

api.add_resource(Question, "/api/questions/<string:slug>")
api.add_resource(CreateListQuestion, "/api/questions")
api.add_resource(CreateAnswer, "/api/questions/<string:slug>/answer")
api.add_resource(Answer, "/api/answers/<int:id>")
api.add_resource(ListAnswer, "/api/answers")

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000, debug=True)

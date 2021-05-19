import traceback
import os

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity

from libs import image_helper
from libs.strings import gettext
from schemas.image import ImageSchema
from models.user import UserModel
from schemas.user import UserSchema

image_schema = ImageSchema()
user_schema = UserSchema()


class UploadAvatar(Resource):
    """
    Upload Avatar - PUT: /upload/avatar
    """
    @fresh_jwt_required
    def put(self):
        """
        Avatars are named in such format: user_{id}.{ext}.
        It will overwrite the existing avatar.
        """
        data = image_schema.load(request.files)
        filename = f"user_{get_jwt_identity()}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": gettext("avatar_delete_failed")}, 500

        try:
            ext = image_helper.get_extension(data["image"].filename)
            _avatar = filename + ext  # use our naming format + true extension
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=_avatar
            )
            basename = image_helper.get_basename(avatar_path)

            full_path = request.host_url + "image/" + basename
            user = UserModel.find_by_id(get_jwt_identity())
            user.avatar = full_path
            user.save_to_db()

            return {"message": gettext("avatar_uploaded").format(basename)}, 200
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Avatar(Resource):
    """
    Get Avatar by User Id - GET: /user/avatar/<int:user_id>
    """
    @classmethod
    def get(cls, user_id: int):
        """
        Returns the avatar of the user specified by user_id.
        """
        folder = "avatars"
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            return send_file(avatar)
        return {"message": gettext("avatar_not_found")}, 404


class Image(Resource):
    """
    Get Image by filename - GET: /image/<str:filename>
    """
    def get(self, filename: str):
        """
        This endpoint returns the requested image if exists.
        """
        folder = "avatars"
        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_file_name").format(filename)}, 400
        try:
            # send the requested file with status code 200
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("avatar_not_found").format(filename)}, 404

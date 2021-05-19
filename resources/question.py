from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

from models.question import QuestionModel
from schemas.question import QuestionSchema
from libs.wrapper import self_only
from libs.strings import gettext

question_schema = QuestionSchema()
question_list_schema = QuestionSchema(many=True)


class CreateListQuestion(Resource):
    """
    Create a Question - POST: /questions

    List all Questions - GET: /questions
    """
    @classmethod
    @fresh_jwt_required
    def post(cls):
        question_json = request.get_json()
        question_json["user_id"] = get_jwt_identity()
        question = question_schema.load(question_json)

        try:
            question.save_to_db()
        except:
            return {"message": gettext("server_error")}, 500

        return question_schema.dump(question), 201

    @classmethod
    def get(cls):
        return question_list_schema.dump(QuestionModel.find_all()), 200


class Question(Resource):
    """
    Get Question by slug - GET: /questions/<string:slug>

    Update Question by slug - PUT: /questions/<string:slug>

    Delete Question by slug - DELETE: /questions/<string:slug>
    """
    @classmethod
    def get(cls, slug: str):
        question = QuestionModel.find_by_slug(slug)
        if question:
            return question_schema.dump(question), 200

        return {"message": gettext("question_not_found").format(slug)}, 404

    @classmethod
    @jwt_required
    def put(cls, slug: str):
        question_json = request.get_json()
        question_json["user_id"] = g.user.id

        question = QuestionModel.find_by_slug(slug)
        if question:
            question.content = item_json["content"]
        else:
            question = question_schema.load(question_json)

        try:
            question.save_to_db()
        except:
            return {"message": gettext("server_error")}, 500

        return question_schema.dump(question), 200

    @classmethod
    @jwt_required
    def delete(cls, slug: str):
        question = QuestionModel.find_by_slug(slug)
        if question:
            question.delete_from_db()
           return {"message": gettext("question_deleted")}, 200

       return {"message": gettext("question_not_found").format(slug)}, 404

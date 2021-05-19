from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

from models.answer import AnswerModel
from models.question import QuestionModel
from schemas.answer import AnswerSchema
from libs.wrapper import self_only
from libs.strings import gettext

answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)


class CreateAnswer(Resource):
    """
    Create an Answer by Question slug - POST: /questions/<string:slug>/answer
    """
    @classmethod
    @fresh_jwt_required
    def post(cls, slug: str):
        answer_json = request.get_json()

        if QuestionModel.find_by_slug(slug) is None:
        return {"message": gettext("question_not_found").format(slug)}, 400

        question = QuestionModel.find_by_slug(slug)
        answer_json["question_id"] = question.id

        answer_json["user_id"] = get_jwt_identity()
        if AnswerModel.find_by_user_id(get_jwt_identity()):
        return {"message": gettext("user_not_found")}, 400

        answer = answer_schema.load(answer_json)

        try:
            answer.save_to_db()
        except:
            return {"message": gettext("server_error")}, 500

        return answer_schema.dump(answer), 201


class Answer(Resource):
    """
    Get an Answer by Id - GET: /answers/<int:id>

    Delete an Answer by Id - DELETE: /answers/<int:id>

    Update an Answer by Id - PUT: /answers/<int:id>
    """
    @classmethod
    def get(cls, id: str):
        answer = AnswerModel.find_by_id(id)
        if answer:
            return answer_schema.dump(answer), 200

        return {"message": gettext("answer_not_found")}, 404

    @classmethod
    @jwt_required
    def delete(cls, id: str):
        answer = AnswerModel.find_by_id(id)
        if answer:
            answer.delete_from_db()
            return {"message": gettext("answer_deleted")}, 200

        return {"message": gettext("answer_not_found")}, 404

    @classmethod
    @jwt_required
    def put(cls, id: str):
        answer_json = request.get_json()

        answer = AnswerModel.find_by_id(id)
        if answer:
            answer.content = answer_json["content"]
        else:
            answer_json["id"] = id
            answer = answer_schema.load(answer_json)

        answer.save_to_db()

        return answer_schema.dump(answer), 200


class ListAnswer(Resource):
    @classmethod
    def get(cls):
        return answer_list_schema.dump(AnswerModel.find_all()), 200

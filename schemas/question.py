from ma import ma
from models.question import QuestionModel
from models.answer import AnswerModel
from schemas.answer import AnswerSchema


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    answers = ma.Nested(AnswerSchema, many=True)

    class Meta:
        model = QuestionModel
        dump_only = ("id", "created_at", "slug",)
        include_fk = True
        load_instance = True
        
    author = ma.Function(lambda obj: obj.user.name)
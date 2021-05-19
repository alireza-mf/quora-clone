from ma import ma
from models.answer import AnswerModel
from models.question import QuestionModel


class AnswerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AnswerModel
        dump_only = ("id","created_at",)
        include_fk = True
        load_instance = True

    author = ma.Function(lambda obj: obj.user.name)
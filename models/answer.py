from datetime import datetime
from typing import List

from db import db



class AnswerModel(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    user = db.relationship("UserModel", backref="answer")
    question = db.relationship("QuestionModel", backref="answer")

    @classmethod
    def find_by_id(cls, id: str) -> "AnswerModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "AnswerModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls) -> List["AnswerModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

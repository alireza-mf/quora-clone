from requests import Response
from datetime import datetime
from flask import request, url_for
from werkzeug.security import generate_password_hash

from db import db
from libs.mailgun import Mailgun
from models.question import QuestionModel
from models.answer import AnswerModel
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar = db.Column(db.String(128))

    questions = db.relationship("QuestionModel", lazy="dynamic", cascade="all, delete-orphan")
    answers = db.relationship("AnswerModel", lazy="dynamic", cascade="all, delete-orphan")

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        # ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_by_id(cls, id: str) -> "UserModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    def send_confirmation_email(self) -> Response:
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation.id
        )
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

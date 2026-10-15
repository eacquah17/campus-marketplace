from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from extensions import db 



    

class User (db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable = False)
    username = db.Column(db.String(30), nullable = False)
    hashed_password = db.Column(db.String(255), nullable = False)
    # listings: Mapped[List["Listing"]] = relationship(back_populates="user", lazy="selectin")
    # cognito_sub = db.Column(db.String(120), unique=True, nullable=False)
    # cognito_sub = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password, method="pbkdf2")

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password, method="pbkdf2")

class Listing(db.Model):

    __tablename__ = "listings"
    id = db.Column(db.Integer, primary_key=True)
    # user: Mapped["User"] = relationship(back_populates="listings") #created a realtionship with the user to make it easier to add the rest of the CRUD operations in the future
    #user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from bson import ObjectId
from lbUser.ConfirmationCodeLbUser import ConfirmationCodeLbUser
from lbUser.EnumStatusLbUser import EnumStatusLbUser
from lbUser.AddressLbUser import AddressLbUser
from pydantic import BaseModel
from pydantic import Field
from typing import List


class LbUser(BaseModel):

    id: ObjectId = Field(
        description="Object id user at mongo database",
        default=None,
        alias="_id"
    )

    registration_date: int = Field(
        description="Registration date user at mongo database",
        default=None
    )

    username: str = Field(
        description="Username user at mongo database",
        default=None
    )

    name: str = Field(
        description="Name user at mongo database",
        default=None
    )

    email: str = Field(
        description="Email user at mongo database",
        default=None
    )

    phone: str = Field(
        description="Phone user at mongo database",
        default=None
    )

    sex: str = Field(
        description="Sex user at mongo database",
        default=None
    )

    birth_date: str = Field(
        description="Birth date user at mongo database",
        default=None
    )

    status: EnumStatusLbUser = Field(
        description="Status user at mongo database",
        default=None
    )

    address: AddressLbUser = Field(
        description="Address user at mongo database",
        default=None
    )

    salt: str = Field(
        description="Salt user at mongo database",
        default=None
    )

    digest: str = Field(
        description="Digest user at mongo database",
        default=None
    )

    confirmation_code: ConfirmationCodeLbUser = Field(
        description="Confirmation code user at mongo database",
        default=None
    )

    permissions: List[str] = Field(
        description="List with user permissions at mongo database",
        default=None
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

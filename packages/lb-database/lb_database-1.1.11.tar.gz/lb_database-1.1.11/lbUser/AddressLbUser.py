# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from pydantic import BaseModel
from pydantic import Field


class AddressLbUser(BaseModel):

    street: str = Field(
        description="Street address user at mongo database",
        default=None
    )

    zipcode: str = Field(
        description="Zipcode address user at mongo database",
        default=None
    )

    city: str = Field(
        description="City address user at mongo database",
        default=None
    )

    state: str = Field(
        description="State address user at mongo database",
        default=None
    )

    district: str = Field(
        description="District address user at mongo database",
        default=None
    )

    number: str = Field(
        description="Number address user at mongo database",
        default=None
    )

    country: str = Field(
        description="Country address user at mongo database",
        default=None
    )

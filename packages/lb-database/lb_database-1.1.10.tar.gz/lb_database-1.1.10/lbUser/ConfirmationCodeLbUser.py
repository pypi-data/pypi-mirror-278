# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from pydantic import BaseModel
from pydantic import Field


class ConfirmationCodeLbUser(BaseModel):

    code: str = Field(
        description="Code confirmation code user at mongo database",
        default=None
    )

    validity: int = Field(
        description="Validity confirmation code user at mongo database",
        default=None
    )

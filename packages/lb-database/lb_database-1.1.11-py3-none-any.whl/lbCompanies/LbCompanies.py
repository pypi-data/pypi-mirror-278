# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class LbCompanies(BaseModel):

    id: ObjectId = Field(
        description="Object id company at mongo database",
        default=None,
        alias="_id"
    )

    basic_cnpj: str = Field(
        description="Basic CNPJ (First 8 digits) company at mongo database",
        default=None
    )

    cnpj: str = Field(
        description="CNPJ (First 8 digits) company at mongo database",
        default=None
    )

    cnpj_digit: str = Field(
        description="Check digit company at mongo database",
        default=None
    )

    identification_code: str = Field(
        description="Identification code company at mongo database",
        default=None
    )

    fantasy_name: str = Field(
        description="Fantasy name company at mongo database",
        default=None
    )

    social_name: str = Field(
        description="Social name company at mongo database",
        default=None
    )

    legal_nature: str = Field(
        description="Legal nature company at mongo database",
        default=None
    )

    qualification_of_responsible: str = Field(
        description="Qualification of responsible company at mongo database",
        default=None
    )

    share_capital: float = Field(
        description="Share capital company at mongo database",
        default=None
    )

    company_size: str = Field(
        description="Size company at mongo database",
        default=None
    )

    federal_entity: str = Field(
        description="Federal entity company at mongo database",
        default=None
    )

    registration_situation: str = Field(
        description="Registration situation company at mongo database",
        default=None
    )

    registration_situation_date: int = Field(
        description="Date registration situation company at mongo database",
        default=None
    )

    registration_situation_motive: str = Field(
        description="Motive registration situation company at mongo database",
        default=None
    )

    city: str = Field(
        description="City company at mongo database",
        default=None
    )

    country: str = Field(
        description="Country company at mongo database",
        default=None
    )

    registration_date: int = Field(
        description="Registration date company at mongo database",
        default=None
    )

    main_cnae: str = Field(
        description="Main CNAE company at mongo database",
        default=None
    )

    secondary_cnae: str = Field(
        description="Secondary cnae company at mongo database",
        default=None
    )

    type_street: str = Field(
        description="Type street company at mongo database",
        default=None
    )

    street: str = Field(
        description="Street company at mongo database",
        default=None
    )

    number: str = Field(
        description="Number company at mongo database",
        default=None
    )

    complement: str = Field(
        description="Complement company at mongo database",
        default=None
    )

    district: str = Field(
        description="District company at mongo database",
        default=None
    )

    zipcode: str = Field(
        description="Zip code company at mongo database",
        default=None
    )

    state: str = Field(
        description="State company at mongo database",
        default=None
    )

    county: str = Field(
        description="County company at mongo database",
        default=None
    )

    ddd: str = Field(
        description="DDD phone company at mongo database",
        default=None
    )

    phone: str = Field(
        description="Phone company at mongo database",
        default=None
    )

    second_ddd: str = Field(
        description="Second DDD phone company at mongo database",
        default=None
    )

    second_phone: str = Field(
        description="Second phone company at mongo database",
        default=None
    )

    fax_ddd: str = Field(
        description="Fax DDD phone company at mongo database",
        default=None
    )

    fax: str = Field(
        description="Fax company at mongo database",
        default=None
    )

    mail: str = Field(
        description="Mail company at mongo database",
        default=None
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

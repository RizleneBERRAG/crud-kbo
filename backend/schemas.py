from typing import Optional, List
from pydantic import BaseModel


# ---------- Establishment (succursale) ----------

class EstablishmentBase(BaseModel):
    name: str
    street: Optional[str] = None
    number: Optional[str] = None
    postcode: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = "Belgium"


class EstablishmentCreate(EstablishmentBase):
    pass


class EstablishmentRead(EstablishmentBase):
    id: int
    establishment_number: Optional[str] = None

    class Config:
        orm_mode = True


# ---------- Company (entreprise) ----------

class CompanyBase(BaseModel):
    name: str
    legal_form: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    postcode: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = "Belgium"
    activity_code: Optional[str] = None
    enterprise_number: Optional[str] = None  # numéro BCE facultatif


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    legal_form: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    postcode: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    activity_code: Optional[str] = None
    enterprise_number: Optional[str] = None


class CompanyRead(CompanyBase):
    id: int
    establishments: List[EstablishmentRead] = []

    class Config:
        orm_mode = True

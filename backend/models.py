from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    nace_code = Column(String, index=True, nullable=False)
    activity_group = Column(String, nullable=True)
    nace_version = Column(String, nullable=True)
    classification = Column(String, nullable=True)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    enterprise_number = Column(String, unique=True, index=True, nullable=True)  # numéro BCE
    name = Column(String, nullable=False)
    legal_form = Column(String, nullable=True)

    street = Column(String, nullable=True)
    number = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, default="Belgium")

    activity_code = Column(String, nullable=True)  # code d'activité (NACEBEL simplifié)

    # Relation 1 -> N avec les unités d'établissement
    establishments = relationship(
        "Establishment",
        back_populates="company",
        cascade="all, delete-orphan"
    )


class Establishment(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True, index=True)
    establishment_number = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)

    street = Column(String, nullable=True)
    number = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, default="Belgium")

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )

    company = relationship("Company", back_populates="establishments")

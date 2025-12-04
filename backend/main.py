from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models
from . import schemas

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD KBO")


@app.get("/ping")
def ping():
    return {"message": "pong"}


# -------------------- CRUD ENTREPRISES --------------------


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas


@app.post("/companies", response_model=schemas.CompanyRead)
def create_company(payload: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """
    Crée une entreprise.
    - Si activity_code est fourni, on vérifie qu'il existe dans la table Activity.
    - On vérifie aussi que le numéro d'entreprise n'est pas déjà utilisé.
    """

    # 1) Vérifier le code NACE si renseigné
    if payload.activity_code:
        activity = (
            db.query(models.Activity)
            .filter(models.Activity.nace_code == payload.activity_code)
            .first()
        )
        if activity is None:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Activité '{payload.activity_code}' inconnue. "
                    "Veuillez utiliser un code NACE valide issu des données KBO."
                ),
            )

    # 2) Vérifier l'unicité du numéro d'entreprise
    existing_company = (
        db.query(models.Company)
        .filter(models.Company.enterprise_number == payload.enterprise_number)
        .first()
    )
    if existing_company:
        raise HTTPException(
            status_code=400,
            detail=(
                f"L'entreprise avec le numéro {payload.enterprise_number} "
                "existe déjà."
            ),
        )

    # 3) Créer et sauvegarder l'entreprise
    company = models.Company(**payload.dict())
    db.add(company)
    db.commit()
    db.refresh(company)

    return company




@app.get("/companies", response_model=List[schemas.CompanyRead])
def list_companies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    companies = db.query(models.Company).offset(skip).limit(limit).all()
    return companies


@app.get("/companies/{company_id}", response_model=schemas.CompanyRead)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")
    return company


@app.put("/companies/{company_id}", response_model=schemas.CompanyRead)
def update_company(
    company_id: int,
    company_in: schemas.CompanyUpdate,
    db: Session = Depends(get_db),
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")

    update_data = company_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


@app.delete("/companies/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")

    db.delete(company)
    db.commit()
    return {"detail": "Entreprise supprimée"}
# -------------------- CRUD ESTABLISHMENTS --------------------


@app.post(
    "/companies/{company_id}/establishments",
    response_model=schemas.EstablishmentRead,
)
def create_establishment_for_company(
    company_id: int,
    establishment_in: schemas.EstablishmentCreate,
    db: Session = Depends(get_db),
):
    """Créer une succursale pour une entreprise donnée."""
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")

    est = models.Establishment(
        company_id=company_id,
        **establishment_in.dict(),
    )
    db.add(est)
    db.commit()
    db.refresh(est)
    return est


@app.get(
    "/companies/{company_id}/establishments",
    response_model=List[schemas.EstablishmentRead],
)
def list_establishments_for_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    """Lister les succursales d'une entreprise."""
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")

    return company.establishments


@app.get(
    "/establishments/{establishment_id}",
    response_model=schemas.EstablishmentRead,
)
def get_establishment(
    establishment_id: int,
    db: Session = Depends(get_db),
):
    """Lire une succursale par son id."""
    est = (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )
    if not est:
        raise HTTPException(status_code=404, detail="Succursale non trouvée")
    return est


@app.put(
    "/establishments/{establishment_id}",
    response_model=schemas.EstablishmentRead,
)
def update_establishment(
    establishment_id: int,
    establishment_in: schemas.EstablishmentCreate,
    db: Session = Depends(get_db),
):
    """Mettre à jour une succursale."""
    est = (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )
    if not est:
        raise HTTPException(status_code=404, detail="Succursale non trouvée")

    for field, value in establishment_in.dict().items():
        setattr(est, field, value)

    db.commit()
    db.refresh(est)
    return est


@app.delete("/establishments/{establishment_id}")
def delete_establishment(
    establishment_id: int,
    db: Session = Depends(get_db),
):
    """Supprimer une succursale."""
    est = (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )
    if not est:
        raise HTTPException(status_code=404, detail="Succursale non trouvée")

    db.delete(est)
    db.commit()
    return {"detail": "Succursale supprimée"}

import csv
from pathlib import Path

from .database import SessionLocal
from . import models

DATA_DIR = Path("data")  # dossier contenant enterprise.csv, establishment.csv


def import_companies(max_rows: int = 50):
    """Importe quelques entreprises depuis enterprise.csv."""
    csv_path = DATA_DIR / "enterprise.csv"
    if not csv_path.exists():
        print(f"[ERREUR] Fichier introuvable : {csv_path}")
        return

    db = SessionLocal()
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            # Ici le séparateur est la virgule
            reader = csv.DictReader(f, delimiter=",")

            print("[enterprise.csv] Colonnes :", reader.fieldnames)

            count = 0
            for row in reader:
                # Vrai nom de colonne : EnterpriseNumber
                enterprise_number = row.get("EnterpriseNumber")
                if not enterprise_number:
                    continue

                legal_form = row.get("JuridicalForm")

                company = models.Company(
                    enterprise_number=enterprise_number,
                    name=f"Entreprise {enterprise_number}",
                    legal_form=legal_form,
                    country="Belgium",
                )
                db.add(company)
                count += 1

                if count >= max_rows:
                    break

            db.commit()

        print(f"[OK] {count} entreprises importées depuis {csv_path.name}")

    finally:
        db.close()



def import_establishments(max_rows: int = 50):
    """Importe quelques unités d'établissement depuis establishment.csv."""
    csv_path = DATA_DIR / "establishment.csv"
    if not csv_path.exists():
        print(f"[ERREUR] Fichier introuvable : {csv_path}")
        return

    db = SessionLocal()
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")

            print("[establishment.csv] Colonnes :", reader.fieldnames)

            count = 0
            for row in reader:
                # Vrais noms de colonnes
                establishment_number = row.get("EstablishmentNumber")
                enterprise_number = row.get("EnterpriseNumber")

                if not establishment_number or not enterprise_number:
                    continue

                # Chercher l'entreprise correspondante
                company = (
                    db.query(models.Company)
                    .filter(models.Company.enterprise_number == enterprise_number)
                    .first()
                )
                if not company:
                    continue

                est = models.Establishment(
                    establishment_number=establishment_number,
                    name=f"Etablissement {establishment_number}",
                    company_id=company.id,
                    country="Belgium",
                )

                db.add(est)
                count += 1

                if count >= max_rows:
                    break

            db.commit()

        print(f"[OK] {count} établissements importés depuis {csv_path.name}")

    finally:
        db.close()


def main():
    print("=== Import KBO → SQLite ===")
    import_companies()
    import_establishments()
    print("=== Fin de l'import ===")


if __name__ == "__main__":
    main()

import csv
from pathlib import Path

from .database import SessionLocal
from . import models

DATA_DIR = Path("data")  # dossier contenant activity.csv, enterprise.csv, establishment.csv


def import_activities(max_rows: int = 500):
    """Importe un échantillon d'activités depuis activity.csv."""
    csv_path = DATA_DIR / "activity.csv"
    if not csv_path.exists():
        print(f"[ERREUR] Fichier introuvable : {csv_path}")
        return

    db = SessionLocal()
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            # d'après ton print, séparateur = virgule
            reader = csv.DictReader(f, delimiter=",")

            print("[activity.csv] Colonnes :", reader.fieldnames)

            count = 0
            for row in reader:
                nace_code = (
                    row.get("NaceCode")
                    or row.get("NACECode")
                    or row.get("NACE_CODE")
                    or row.get("Nacecode")
                )
                if not nace_code:
                    continue

                activity_group = row.get("ActivityGroup") or row.get("ACTIVITYGROUP")
                nace_version = row.get("NaceVersion") or row.get("NACEVERSION")
                classification = row.get("Classification") or row.get("CLASSIFICATION")

                # éviter les doublons sur le code NACE
                existing = (
                    db.query(models.Activity)
                    .filter(models.Activity.nace_code == nace_code)
                    .first()
                )
                if existing:
                    continue

                act = models.Activity(
                    nace_code=nace_code,
                    activity_group=activity_group,
                    nace_version=nace_version,
                    classification=classification,
                )
                db.add(act)
                count += 1

                if count >= max_rows:
                    break

            db.commit()

        print(f"[OK] {count} activités importées depuis {csv_path.name}")

    finally:
        db.close()


def import_companies(max_rows: int = 50):
    """Importe quelques entreprises depuis enterprise.csv."""
    csv_path = DATA_DIR / "enterprise.csv"
    if not csv_path.exists():
        print(f"[ERREUR] Fichier introuvable : {csv_path}")
        return

    db = SessionLocal()
    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")

            print("[enterprise.csv] Colonnes :", reader.fieldnames)

            count = 0
            for row in reader:
                enterprise_number = row.get("EnterpriseNumber")
                if not enterprise_number:
                    continue

                # éviter les doublons sur le numéro BCE
                existing = (
                    db.query(models.Company)
                    .filter(models.Company.enterprise_number == enterprise_number)
                    .first()
                )
                if existing:
                    continue

                legal_form = row.get("JuridicalForm")

                company = models.Company(
                    enterprise_number=enterprise_number,
                    name=f"Entreprise {enterprise_number}",
                    legal_form=legal_form,
                    country="Belgium",
                    # activity_code restera None au début (rempli plus tard via l'API)
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
                establishment_number = row.get("EstablishmentNumber")
                enterprise_number = row.get("EnterpriseNumber")

                if not establishment_number or not enterprise_number:
                    continue

                # éviter les doublons sur le n° d'établissement
                existing = (
                    db.query(models.Establishment)
                    .filter(models.Establishment.establishment_number == establishment_number)
                    .first()
                )
                if existing:
                    continue

                # chercher l'entreprise correspondante
                company = (
                    db.query(models.Company)
                    .filter(models.Company.enterprise_number == enterprise_number)
                    .first()
                )
                if not company:
                    # on ignore si l'entreprise n'est pas dans l'échantillon
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
    import_activities()
    import_companies()
    import_establishments()
    print("=== Fin de l'import ===")


if __name__ == "__main__":
    main()
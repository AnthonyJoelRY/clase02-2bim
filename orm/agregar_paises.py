import csv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelo import Pais
from config import cadena_base_datos

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)


def cargar_paises():
    session = Session()
    try:
        nombres = set()
        path = DATA_DIR / "paises.csv"
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nombre = row.get("nombre", "").strip()
                if not nombre or nombre in nombres:
                    continue
                
                # Verificar si el país ya existe
                pais_existente = session.query(Pais).filter_by(nombre=nombre).first()
                if pais_existente:
                    print(f"País '{nombre}' ya existe, omitiendo...")
                    continue
                
                continente = row.get("continente", "").strip() or None
                pais = Pais(nombre=nombre, continente=continente)
                session.add(pais)
                nombres.add(nombre)
        session.commit()
        print(f"Cargados {len(nombres)} paises desde: paises.csv")
    except Exception as e:
        session.rollback()
        print(f"Error al cargar paises: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    cargar_paises()

import csv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelo import Actor, Pais, Serie
from config import cadena_base_datos

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)


def cargar_actores():
    session = Session()
    try:
        actores_agregados = 0
        path = DATA_DIR / "actores.csv"
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nombre = row.get("nombre", "").strip()
                if not nombre:
                    continue
                
                edad = row.get("edad", "").strip()
                edad = int(edad) if edad else None
                
                pais_nombre = row.get("pais", "").strip()
                pais_id = None
                if pais_nombre:
                    pais = session.query(Pais).filter(Pais.nombre.ilike(pais_nombre)).first()
                    if pais:
                        pais_id = pais.id
                
                serie_titulo = row.get("serie", "").strip()
                serie_id = None
                if serie_titulo:
                    serie = session.query(Serie).filter(Serie.titulo.ilike(serie_titulo)).first()
                    if serie:
                        serie_id = serie.id
                
                actor = Actor(
                    nombre=nombre,
                    edad=edad,
                    pais_id=pais_id,
                    serie_id=serie_id
                )
                session.add(actor)
                actores_agregados += 1
        
        session.commit()
        print(f"Cargados {actores_agregados} actores desde: actores.csv")
    except Exception as e:
        session.rollback()
        print(f"Error al cargar actores: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    cargar_actores()

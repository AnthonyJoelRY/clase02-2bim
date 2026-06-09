import csv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelo import Premio, Serie
from config import cadena_base_datos

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)


def cargar_premios():
    session = Session()
    try:
        premios_agregados = 0
        path = DATA_DIR / "premios.csv"
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nombre_premio = row.get("nombre_premio", "").strip()
                if not nombre_premio:
                    continue
                
                categoria = row.get("categoria", "").strip() or None
                
                anio = row.get("anio", "").strip()
                anio = int(anio) if anio else None
                
                serie_titulo = row.get("serie", "").strip()
                serie_id = None
                if serie_titulo:
                    serie = session.query(Serie).filter(Serie.titulo.ilike(serie_titulo)).first()
                    if serie:
                        serie_id = serie.id
                
                premio = Premio(
                    nombre_premio=nombre_premio,
                    categoria=categoria,
                    anio=anio,
                    serie_id=serie_id
                )
                session.add(premio)
                premios_agregados += 1
        
        session.commit()
        print(f"Cargados {premios_agregados} premios desde: premios.csv")
    except Exception as e:
        session.rollback()
        print(f"Error al cargar premios: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    cargar_premios()

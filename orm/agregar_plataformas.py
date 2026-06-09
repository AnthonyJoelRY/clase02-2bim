import csv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelo import Plataforma, Pais
from config import cadena_base_datos

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)


def cargar_plataformas():
    session = Session()
    try:
        nombres = set()
        path = DATA_DIR / "plataformas.csv"
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nombre = row.get("nombre", "").strip()
                if not nombre or nombre in nombres:
                    continue
                
                # Verificar si la plataforma ya existe
                plataforma_existente = session.query(Plataforma).filter_by(nombre=nombre).first()
                if plataforma_existente:
                    print(f"Plataforma '{nombre}' ya existe, omitiendo...")
                    continue
                
                pais_nombre = row.get("pais", "").strip()
                pais_id = None
                if pais_nombre:
                    pais = session.query(Pais).filter(Pais.nombre.ilike(pais_nombre)).first()
                    if pais:
                        pais_id = pais.id
                
                suscriptores = row.get("suscriptores_millones", "").strip()
                suscriptores_millones = None
                if suscriptores:
                    try:
                        suscriptores_millones = int(float(suscriptores))
                    except (ValueError, TypeError):
                        pass
                
                plataforma = Plataforma(
                    nombre=nombre,
                    pais_id=pais_id,
                    suscriptores_millones=suscriptores_millones
                )
                session.add(plataforma)
                nombres.add(nombre)
        
        session.commit()
        print(f"Cargadas {len(nombres)} plataformas desde: plataformas.csv")
    except Exception as e:
        session.rollback()
        print(f"Error al cargar plataformas: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    cargar_plataformas()

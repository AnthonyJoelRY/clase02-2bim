import csv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelo import Serie, Plataforma, Pais
from config import cadena_base_datos

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)


def cargar_series():
    session = Session()
    try:
        titulos = set()
        path = DATA_DIR / "series.csv"
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                titulo = row.get("titulo", "").strip()
                if not titulo or titulo in titulos:
                    continue
                
                # Verificar si la serie ya existe
                serie_existente = session.query(Serie).filter_by(titulo=titulo).first()
                if serie_existente:
                    print(f"Serie '{titulo}' ya existe, omitiendo...")
                    continue
                
                genero = row.get("genero", "").strip() or None
                
                anio_estreno = row.get("anio_estreno", "").strip()
                anio_estreno = int(anio_estreno) if anio_estreno else None
                
                temporadas = row.get("temporadas", "").strip()
                temporadas = int(temporadas) if temporadas else None
                
                plataforma_nombre = row.get("plataforma", "").strip()
                plataforma_id = None
                if plataforma_nombre:
                    plataforma = session.query(Plataforma).filter(Plataforma.nombre.ilike(plataforma_nombre)).first()
                    if plataforma:
                        plataforma_id = plataforma.id
                
                pais_nombre = row.get("pais", "").strip()
                pais_id = None
                if pais_nombre:
                    pais = session.query(Pais).filter(Pais.nombre.ilike(pais_nombre)).first()
                    if pais:
                        pais_id = pais.id
                
                serie = Serie(
                    titulo=titulo,
                    genero=genero,
                    anio_estreno=anio_estreno,
                    temporadas=temporadas,
                    plataforma_id=plataforma_id,
                    pais_id=pais_id
                )
                session.add(serie)
                titulos.add(titulo)
        
        session.commit()
        print(f"Cargadas {len(titulos)} series desde: series.csv")
    except Exception as e:
        session.rollback()
        print(f"Error al cargar series: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    cargar_series()

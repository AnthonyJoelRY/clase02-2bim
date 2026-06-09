import csv
from config import cadena_base_datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo import Serie, Plataforma, Pais

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

with open("data/series.csv", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        plataforma = session.query(Plataforma).filter(Plataforma.nombre.ilike(fila["plataforma"])).first()
        pais = session.query(Pais).filter(Pais.nombre.ilike(fila["pais"])).first()
        
        serie = Serie(
            titulo=fila["titulo"],
            genero=fila["genero"],
            anio_estreno=int(fila["anio_estreno"]),
            temporadas=int(fila["temporadas"]),
            plataforma=plataforma,
            pais=pais
        )
        session.add(serie)

session.commit()
session.close()

print("Series agregadas correctamente")

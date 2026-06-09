import csv
from config import cadena_base_datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo import Plataforma, Pais

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

with open("data/plataformas.csv", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        pais = session.query(Pais).filter(Pais.nombre.ilike(fila["pais"])).first()
        
        plataforma = Plataforma(
            nombre=fila["nombre"],
            pais=pais,
            suscriptores_millones=int(float(fila["suscriptores_millones"]))
        )
        session.add(plataforma)

session.commit()
session.close()

print("Plataformas agregadas correctamente")

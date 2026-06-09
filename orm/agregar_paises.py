import csv
from config import cadena_base_datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo import Pais

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

with open("data/paises.csv", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        pais = Pais(
            nombre=fila["nombre"],
            continente=fila["continente"]
        )
        session.add(pais)

session.commit()
session.close()

print("Paises agregados correctamente")

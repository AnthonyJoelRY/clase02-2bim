import csv
from config import cadena_base_datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo import Actor, Pais, Serie

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

with open("../data/actores.csv", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        pais = session.query(Pais).filter(Pais.nombre.ilike(fila["pais"])).first()
        serie = session.query(Serie).filter(Serie.titulo.ilike(fila["serie"])).first()
        
        actor = Actor(
            nombre=fila["nombre"],
            edad=int(fila["edad"]),
            rol="Actor",
            pais=pais,
            serie=serie
        )
        session.add(actor)

session.commit()
session.close()

print("Actores agregados correctamente")

import csv
from config import cadena_base_datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo import Serie, Premio

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

with open("../data/premios.csv", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        serie = session.query(Serie).filter(Serie.titulo.ilike(fila["serie"])).first()
        
        premio = Premio(
            nombre_premio=fila["nombre_premio"],
            categoria=fila["categoria"],
            anio=int(fila["anio"]),
            serie=serie
        )
        session.add(premio)

session.commit()
session.close()

print("Premios agregados correctamente")

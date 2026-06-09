"""
el titulo de la serie con el promedio de edades de los actores.
el titulo de la serie con el promedio de edades de los actores y numero de premios de la serie 
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelo import Serie
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Obtener todas las series
series = session.query(Serie).all()

print("Título de serie y promedio de edades de actores:")
print("-" * 60)
for serie in series:
    promedio = serie.obtener_edad_actores()
    if promedio > 0:
        print(f"Serie: {serie.titulo}")
        print(f"Promedio de edad: {promedio:.2f}")
        print("-" * 60)

session.close()




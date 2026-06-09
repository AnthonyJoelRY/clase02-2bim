"""
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

print("Título de serie, promedio de edades de actores y número de premios:")
print("-" * 80)
for serie in series:
    promedio_edad = serie.obtener_edad_actores()
    total_premios = serie.obtener_total_premios()
    
    if promedio_edad > 0 or total_premios > 0:
        print(f"Serie: {serie.titulo}")
        print(f"  Promedio de edad: {promedio_edad:.2f}")
        print(f"  Total de premios: {total_premios}")
        print("-" * 80)





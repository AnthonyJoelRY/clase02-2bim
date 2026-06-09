"""
el titulo de la serie con el promedio de edades de los actores.
"""

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from modelo import Serie, Actor
from config import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Consulta: título de la serie con el promedio de edades de los actores
resultados = session.query(
    Serie.titulo,
    func.avg(Actor.edad).label("promedio_edad")
).join(Actor).group_by(Serie.id, Serie.titulo).all()

print("Título de serie y promedio de edades de actores:")
print("-" * 60)
for titulo, promedio in resultados:
    if promedio:
        print(f"Serie: {titulo}")
        print(f"Promedio de edad: {promedio:.2f}")
        print("-" * 60)

session.close()

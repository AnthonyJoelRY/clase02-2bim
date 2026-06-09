from pathlib import Path

# este módulo será usado para posibles configuraciones
#
# cadena conector a la base de datos
#
# Sqlite
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "bd" / "PracticaClase.db"
cadena_base_datos = f"sqlite:///{DB_PATH.as_posix()}"

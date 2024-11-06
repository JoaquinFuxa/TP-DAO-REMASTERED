from classes.servicio import Servicio
from database.database_connection import DatabaseConnection  

class GestorDeServicios:
    _instance = None  # Singleton para GestorDeAutos
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorDeServicios, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de la conexión a la BD
        return cls._instance

   
    def registrar_servicio(self, vin, tipo_servicio, fecha, costo):
        """Registra un nuevo servicio en la base de datos."""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "INSERT INTO servicios (vin, tipo_servicio, fecha, costo) VALUES (?, ?, ?, ?)",
                (vin, tipo_servicio, fecha, costo)
            )
            self.db.get_connection().commit()
            return True
        except Exception as e:
            print(f"Error al registrar servicio: {e}")  # Puedes ver el error en la consola
            self.db.get_connection().rollback()
            return False  # Retorna False si hay un error
        finally:
            cursor.close()

    def obtener_servicios_por_auto(self, vin):
        """Obtiene los detalles de los servicios de un auto específico por su VIN."""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "SELECT id_servicio, vin, tipo_servicio, fecha, costo FROM servicios WHERE vin = ?",
                (vin,)
            )
            resultados = cursor.fetchall()
            servicios = [Servicio(*resultado) for resultado in resultados]  # Crear objetos Servicio
            return servicios  # Retorna una lista de objetos Servicio
        except Exception as e:
            print(f"Error al obtener servicios por auto: {e}")
            return []  # Retorna una lista vacía si hay un error
        finally:
            cursor.close()
    
    def obtener_ingresos_por_servicios(self):
        """Obtiene los ingresos totales por servicios."""
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT SUM(costo) FROM servicios")
        total_servicios = cursor.fetchone()[0] or 0
        cursor.close()
        return total_servicios
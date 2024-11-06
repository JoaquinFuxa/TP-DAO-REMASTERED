from classes.auto import Auto
from database.database_connection import DatabaseConnection  

class GestorDeAutos:
    _instance = None  # Singleton para GestorDeAutos
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorDeAutos, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de la conexión a la BD
        return cls._instance

    def registrar_auto(self, vin, marca, modelo, anio, precio, estado):
        """
        Registra un auto en la base de datos si no existe ya un auto con el mismo VIN.
        """
        try:
            cursor = self.db.get_connection().cursor()
            
            # Comprobar si el auto ya existe
            cursor.execute("SELECT * FROM autos WHERE vin = ?", (vin,))
            if cursor.fetchone() is not None:
                print("El auto con este VIN ya existe.")
                return False  # El auto ya existe
            
            # Registrar el nuevo auto
            cursor.execute(
                "INSERT INTO autos (vin, marca, modelo, anio, precio, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (vin, marca, modelo, anio, precio, estado)
            )
            self.db.get_connection().commit()
            return True  # Inserción exitosa
        except Exception as e:
            print(f"Error al registrar el auto: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()

    def obtener_autos_no_vendidos(self):
        """
        Retorna una lista de autos no vendidos (sin cliente asignado).
        """
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT vin, marca, modelo FROM autos WHERE cliente_id IS NULL")
        autos_no_vendidos = cursor.fetchall()
        cursor.close()
        
        # Transformar los resultados en instancias de Auto
        return [Auto(vin=row[0], marca=row[1], modelo=row[2], anio=None, precio=None, estado='Disponible') for row in autos_no_vendidos]

    def obtener_autos_vendidos(self):
        """
        Retorna una lista de autos vendidos (con cliente asignado).
        """
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT vin, marca, modelo FROM autos WHERE cliente_id IS NOT NULL")
        autos_vendidos = cursor.fetchall()
        cursor.close()
        
        # Transformar los resultados en instancias de Auto
        return [Auto(vin=row[0], marca=row[1], modelo=row[2], anio=None, precio=None, estado='Vendido') for row in autos_vendidos]

    def obtener_autos_vendidos_por_cliente(self, cliente_id):
        """
        Retorna una lista de autos vendidos a un cliente específico.
        """
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT vin, marca, modelo, anio, precio, estado FROM autos WHERE cliente_id = ?", (cliente_id,))
        autos_cliente = cursor.fetchall()
        cursor.close()
        
        # Transformar los resultados en instancias de Auto
        return [Auto(vin=row[0], marca=row[1], modelo=row[2], anio=row[3], precio=row[4], estado=row[5]) for row in autos_cliente]
from classes.auto import Auto
from database.database_connection import DatabaseConnection  
from classes.notificador.notificador import Notificador 


class GestorDeAutos(Notificador):
    _instance = None  # Singleton para GestorDeAutos
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorDeAutos, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de la conexión a la BD
            from gui.interfaz_principal import Aplicacion 
            cls._instance.suscriptor = Aplicacion()
        return cls._instance
    
    def notificar(self):
        self.suscriptor.recibir_notificacion()

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
            self.notificar()
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

    def obtener_autos_mas_vendidos(self):
        """Obtiene los autos más vendidos por marca."""
        cursor = self.db.get_connection().cursor()
        cursor.execute("""
            SELECT a.marca, a.modelo, COUNT(v.id_venta) AS total_ventas
            FROM autos a
            JOIN ventas v ON a.vin = v.vin
            GROUP BY a.marca, a.modelo
            ORDER BY a.marca, total_ventas DESC;
        """)
        autos = cursor.fetchall()
        cursor.close()
        return autos
    
    def obtener_ingresos_por_ventas(self):
        """Obtiene los ingresos totales por ventas de autos."""
        cursor = self.db.get_connection().cursor()
        cursor.execute("""
            SELECT SUM(a.precio) 
            FROM ventas v
            JOIN autos a ON v.vin = a.vin
        """)
        total_ventas = cursor.fetchone()[0] or 0
        cursor.close()
        return total_ventas
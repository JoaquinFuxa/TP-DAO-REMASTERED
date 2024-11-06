from classes.venta import Venta
from database.database_connection import DatabaseConnection  # Asegúrate de que el nombre del archivo coincida

class GestorDeVentas:
    _instance = None  # Singleton para GestorDeVentas
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorDeVentas, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de la conexión a la BD
        return cls._instance

    def registrar_venta(self, vin, cliente, fecha_venta, vendedor, comision):
        """
        Registra una venta de un auto a un cliente por un vendedor, actualizando los datos relacionados en la BD.
        """
        try:
            cursor = self.db.get_connection().cursor()
            
            # Insertar la venta en la tabla de ventas
            cursor.execute("INSERT INTO ventas (vin, cliente_id, fecha_venta, vendedor_id) VALUES (?, ?, ?, ?)",
                           (vin, cliente, fecha_venta, vendedor))
            
            # Actualizar el cliente asociado al auto
            cursor.execute("UPDATE autos SET cliente_id = ? WHERE vin = ?", (cliente, vin))
            
            # Insertar la comisión en la tabla de comisiones
            cursor.execute("INSERT INTO comisiones (vendedor_id, monto, fecha) VALUES (?, ?, ?)",
                           (vendedor, comision, fecha_venta))
            
            # Guardar los cambios en la base de datos
            self.db.get_connection().commit()
            
            return True # Devolvemos el objeto venta si se registró correctamente
        except Exception as e:
            print(f"Error al registrar venta: {e}")
            self.db.get_connection().rollback()
            return None
        
    def obtener_ventas_por_periodo(self, fecha_inicio, fecha_fin):
        """Obtiene las ventas dentro de un rango de fechas."""
        cursor = self.db.get_connection().cursor()
        cursor.execute("""
            SELECT id_venta, vin, cliente_id, fecha_venta, vendedor_id
            FROM ventas
            WHERE strftime('%Y-%m-%d', fecha_venta) BETWEEN strftime('%Y-%m-%d', ?) AND strftime('%Y-%m-%d', ?)
        """, (fecha_inicio, fecha_fin))
        ventas = cursor.fetchall()
        print(ventas)
        cursor.close()
        return ventas
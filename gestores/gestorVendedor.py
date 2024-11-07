from database.database_connection import DatabaseConnection 
from classes.vendedor import Vendedor
from classes.notificador.notificador import Notificador  


class GestorDeVendedores(Notificador):
    _instance = None  # Variable de clase para almacenar la instancia única

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorDeVendedores, cls).__new__(cls)
            cls._instance.db = DatabaseConnection()  # Instancia única de conexión a la base de datos
            from gui.interfaz_principal import Aplicacion 
            cls._instance.suscriptor = Aplicacion()
        return cls._instance
    
    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar_vendedor(self, nombre, apellido, comisiones=0):
        """Registra un nuevo vendedor en la base de datos."""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "INSERT INTO vendedores (nombre, apellido, comisiones) VALUES (?, ?, ?)",
                (nombre, apellido, comisiones)
            )
            self.db.get_connection().commit()
            self.notificar()
            return True
        except Exception as e:
            print(f"Error al registrar vendedor: {e}")
            return False

    def obtener_vendedores(self):
        """Obtiene una lista de todos los vendedores registrados en la base de datos."""
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute("SELECT id_vendedor, nombre, apellido FROM vendedores")
            vendedores_data = cursor.fetchall()
            self.db.get_connection().commit()
            # Crear una lista de objetos Vendedor a partir de los datos obtenidos
            vendedores = [
                Vendedor(id_vendedor, nombre, apellido) 
                for id_vendedor, nombre, apellido in vendedores_data
            ]
            return vendedores
        except Exception as e:
            print(f"Error al obtener vendedores: {e}")
            return []


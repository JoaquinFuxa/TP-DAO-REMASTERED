from classes.cliente import Cliente 
from database.database_connection import DatabaseConnection
from classes.notificador.notificador import Notificador  


class GestorDeClientes(Notificador):
    _instance = None  # Singleton para GestorDeClientes
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorDeClientes, cls).__new__(cls)
            cls._instance.db = DatabaseConnection() # Instancia única de la conexión a la BD
            from gui.interfaz_principal import Aplicacion 
            cls._instance.suscriptor = Aplicacion()
        return cls._instance
    
    def notificar(self):
        self.suscriptor.recibir_notificacion()

    def registrar_cliente(self, nombre, apellido, direccion, telefono):
        """
        Registra un nuevo cliente en la base de datos.
        """
        try:
            cursor = self.db.get_connection().cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, apellido, direccion, telefono) VALUES (?, ?, ?, ?)",
                (nombre, apellido, direccion, telefono)
            )
            self.db.get_connection().commit()
            self.notificar()
            return True  # Inserción exitosa
        except Exception as e:
            print(f"Error al registrar el cliente: {e}")
            self.db.get_connection().rollback()
            return False
        finally:
            cursor.close()

    def obtener_clientes(self):
        """
        Retorna una lista de todos los clientes en la base de datos.
        """
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT id_cliente, nombre, apellido, direccion, telefono FROM clientes")
        clientes_data = cursor.fetchall()
        cursor.close()
        
        # Transformar los resultados en instancias de Cliente
        clientes = [Cliente(id_cliente=row[0], nombre=row[1], apellido=row[2], direccion=row[3], telefono=row[4]) for row in clientes_data]
        return clientes

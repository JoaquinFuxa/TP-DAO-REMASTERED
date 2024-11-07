from tkinter import ttk
from gui.interfaz_registro_auto import InterfazRegistroAuto
from gui.interfaz_registro_cliente import InterfazRegistroCliente
from gui.interfaz_registro_vendedor import InterfazRegistroVendedor
from gui.interfaz_registro_venta import InterfazRegistroVenta
from gui.interfaz_registro_servicio import InterfazRegistroServicio
from gui.interfaz_consulta_autos_vendidos import InterfazConsultaAutosVendidos
from gui.interfaz_consulta_servicios import InterfazConsultaServiciosAuto
from gui.interfaz_reportes import InterfazReportes
from classes.notificador.suscriptor import Suscriptor

class Aplicacion(Suscriptor):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def cargar_ventanas(self, active_index=0):
        for tab in self.contenedor.tabs():
            self.contenedor.forget(tab)
        
        print("CREE MUCHAS VENTANAS")
        # Crear las diferentes páginas
        self.frame_auto = InterfazRegistroAuto(self.contenedor)
        self.frame_cliente = InterfazRegistroCliente(self.contenedor)
        self.frame_vendedor = InterfazRegistroVendedor(self.contenedor)
        self.frame_venta = InterfazRegistroVenta(self.contenedor)
        self.frame_servicio = InterfazRegistroServicio(self.contenedor)
        self.frame_autos_vendidos = InterfazConsultaAutosVendidos(self.contenedor)
        self.frame_servicio_auto = InterfazConsultaServiciosAuto(self.contenedor)
        self.frame_reportes = InterfazReportes(self.contenedor)

        # Agregar las páginas al contenedor
        self.contenedor.add(self.frame_auto, text="Registrar Auto")
        self.contenedor.add(self.frame_cliente, text="Registrar Cliente")
        self.contenedor.add(self.frame_vendedor, text="Registrar Vendedor")
        self.contenedor.add(self.frame_venta, text="Registrar Venta")
        self.contenedor.add(self.frame_servicio, text="Registrar Servicio")
        self.contenedor.add(self.frame_autos_vendidos, text="Consultar Autos")
        self.contenedor.add(self.frame_servicio_auto, text="Consultar Servicio")
        self.contenedor.add(self.frame_reportes, text="Reportes")

        # Volver a la pestaña activa antes de recargar
        self.contenedor.select(active_index)

    def _initialize(self, root):
        self.root = root
        self.root.title("Concesionaria de Autos")

        # Crear estilo
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", padding=5)

        # Crear el contenedor principal (Notebook)
        self.contenedor = ttk.Notebook(root)
        self.contenedor.pack(expand=1, fill='both')

        self.cargar_ventanas()

    def recibir_notificacion(self):
        # Guardar la pestaña activa actual
        active_index = self.contenedor.index(self.contenedor.select())
        # Recargar ventanas manteniendo la pestaña activa
        self.cargar_ventanas(active_index)

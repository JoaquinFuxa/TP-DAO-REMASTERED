import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
from datetime import datetime
from gestores.gestorAuto import GestorDeAutos  # Asegúrate de importar los gestores correspondientes
from gestores.gestorServicio import GestorDeServicios

class InterfazRegistroServicio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancias de los gestores
        self.gestor_servicios = GestorDeServicios()  # Gestor para los servicios
        self.gestor_autos = GestorDeAutos()  # Gestor para los autos

        # Configuración del estilo
        estilo = ttk.Style()
        estilo.configure("TFrame", background="#f2f2f2")
        estilo.configure("TLabel", background="#f2f2f2", font=("Arial", 10, "bold"))
        estilo.configure("TEntry", padding=5, font=("Arial", 10))
        estilo.configure("TCombobox", padding=5, font=("Arial", 10))
        estilo.configure("TButton", background="#007ACC", foreground="white", font=("Arial", 10, "bold"))

        # Crear los elementos de la interfaz con estilo y espaciado
        ttk.Label(self, text="Auto (VIN):").grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.combo_auto = ttk.Combobox(self, state="readonly")
        self.combo_auto.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.cargar_autos()

        # Combobox para seleccionar "Descripción del Servicio"
        ttk.Label(self, text="Descripción del Servicio:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combo_descripcion = ttk.Combobox(self, state="readonly", values=["Mantenimiento", "Reparación"])
        self.combo_descripcion.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Campo de entrada para el costo
        ttk.Label(self, text="Costo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_costo = ttk.Entry(self)
        self.entry_costo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Campo de entrada para la fecha
        ttk.Label(self, text="Fecha (dd/mm/yyyy):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_fecha = ttk.Entry(self)
        self.entry_fecha.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Botón de registro con estilo
        self.boton_registrar = ttk.Button(self, text="Registrar Servicio", command=self.registrar)
        self.boton_registrar.grid(row=4, columnspan=2, pady=(20, 10), padx=10)

        # Expande la segunda columna para ajustarse al tamaño de la ventana
        self.columnconfigure(1, weight=1)

    def cargar_autos(self):
        """Carga los autos vendidos en el Combobox."""
        autos = self.gestor_autos.obtener_autos_vendidos()  # Llamada al gestor para obtener los autos vendidos
        self.combo_auto['values'] = [auto.vin for auto in autos]  # Usamos el VIN del objeto Auto

    def validar_fecha(self, fecha):
        """Valida que la fecha esté en formato dd/mm/yyyy."""
        regex = r'^\d{2}/\d{2}/\d{4}$'
        if re.match(regex, fecha):
            try:
                dia, mes, anio = map(int, fecha.split('/'))
                datetime(anio, mes, dia)  # Si no es una fecha válida, se lanzará una excepción
                return True
            except ValueError:
                return False  # La fecha no es válida
        return False  # No coincide con el formato

    def registrar(self):
        """Registra un servicio para un auto."""
        vin = self.combo_auto.get()
        descripcion = self.combo_descripcion.get()
        
        # Validación de entrada para el costo
        try:
            costo = float(self.entry_costo.get())
        except ValueError:
            messagebox.showerror("Error", "El costo debe ser un número válido.")
            return
        
        fecha = self.entry_fecha.get()  # Obtener la fecha ingresada

        # Validar que todos los campos estén llenos
        if not vin or not descripcion or costo <= 0 or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios y el costo debe ser positivo.")
            return

        # Validar el formato de la fecha
        if not self.validar_fecha(fecha):
            messagebox.showerror("Error", "La fecha debe estar en formato dd/mm/yyyy.")
            return
        
        # Convertir fecha al formato correcto YYYY-MM-DD
        fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Registrar el servicio usando el gestor de servicios
        if self.gestor_servicios.registrar_servicio(vin, descripcion, fecha, costo):
            messagebox.showinfo("Éxito", "Servicio registrado con éxito.")
            self.combo_auto.set('')  # Limpiar la selección de auto
            self.combo_descripcion.set('')  # Limpiar la selección de descripción
            self.entry_costo.delete(0, tk.END)  # Limpiar el campo de costo
            self.entry_fecha.delete(0, tk.END)  # Limpiar el campo de fecha
        else:
            messagebox.showerror("Error", "No se pudo registrar el servicio.")

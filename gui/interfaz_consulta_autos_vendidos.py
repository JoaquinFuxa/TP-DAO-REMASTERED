import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from gestores.gestorCliente import GestorDeClientes  # Importar los gestores
from gestores.gestorAuto import GestorDeAutos

class InterfazConsultaAutosVendidos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear instancias de los gestores
        self.gestor_clientes = GestorDeClientes()  # Gestor de clientes
        self.gestor_autos = GestorDeAutos()  # Gestor de autos

        # Título
        ttk.Label(self, text="Consulta de Autos Vendidos a un Cliente", font=("Arial", 14, "bold")).grid(row=0, columnspan=2, pady=(10, 10))

        # Cliente selector
        ttk.Label(self, text="Cliente:").grid(row=1, column=0, pady=(5, 5), padx=(10, 5))
        self.combo_cliente = ttk.Combobox(self, state='readonly')
        self.combo_cliente.grid(row=1, column=1, pady=(5, 5), padx=(5, 10))
        self.cargar_clientes()

        # Botón para mostrar autos vendidos
        self.boton_mostrar = ttk.Button(self, text="Mostrar Autos Vendidos", command=self.mostrar_autos_vendidos)
        self.boton_mostrar.grid(row=2, columnspan=2, pady=(10, 10))

        # Tabla para mostrar autos vendidos
        columnas = ["vin", "marca", "modelo", "año", "precio", "estado"]
        self.treeview = ttk.Treeview(self, columns=columnas, show='headings', height=8)
        self.treeview.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10))

        # Configurar encabezados y ancho de las columnas
        col_ancho = {
            "vin": 100,
            "marca": 100,
            "modelo": 100,
            "año": 70,
            "precio": 80,
            "estado": 100
        }

        for col in columnas:
            self.treeview.heading(col, text=col.capitalize())
            self.treeview.column(col, anchor="center", width=col_ancho[col])

        # Estilo de los widgets
        estilo = ttk.Style()
        estilo.configure("TButton", background="lightblue", foreground="black", padding=10, font=("Arial", 10, "bold"))

    def cargar_clientes(self):
        """Cargar los clientes en el combo de selección"""
        clientes = self.gestor_clientes.obtener_clientes()  # Obtener clientes usando el gestor
        self.combo_cliente['values'] = [f"{cliente.id_cliente} - {cliente.nombre} {cliente.apellido}" for cliente in clientes]

    def mostrar_autos_vendidos(self):
        """Mostrar los autos vendidos a un cliente seleccionado"""
        cliente_info = self.combo_cliente.get()

        if not cliente_info:
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")
            return

        # Obtener el ID del cliente (antes se manejaba como string, ahora como objeto cliente)
        cliente_id = cliente_info.split(" - ")[0]  # Obtener el ID del cliente

        # Limpiar datos anteriores en la tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Obtener los autos vendidos al cliente
        autos = self.gestor_autos.obtener_autos_vendidos_por_cliente(cliente_id)

        if autos:
            for auto in autos:
                self.treeview.insert("", "end", values=(auto.vin, auto.marca, auto.modelo, auto.anio, auto.precio, auto.estado))
        else:
            messagebox.showinfo("Información", "No hay autos vendidos a este cliente.")

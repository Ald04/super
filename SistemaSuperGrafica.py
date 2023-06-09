import mysql.connector
from tabulate import tabulate
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="supermercado"
)
cursor = db.cursor(buffered=True)

# Crear ventana principal
window = tk.Tk()
window.title("Punto de Compra y Venta")
window.geometry("500x500")
window.resizable(False, False)
window.configure(bg="#F5F5F5")

# Función para mostrar los productos disponibles
def mostrar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    headers = ["ID", "Nombre", "Precio", "Stock"]
    messagebox.showinfo("Productos Disponibles", tabulate(productos, headers=headers))


# Función para agregar un nuevo producto
def agregar_producto():
    def agregar():
        nombre = nombre_entry.get()
        precio = float(precio_entry.get())
        stock = int(stock_entry.get())

        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
        db.commit()

        messagebox.showinfo("Producto Agregado", "Producto agregado exitosamente")

    agregar_window = tk.Toplevel(window)
    agregar_window.title("Agregar Producto")
    agregar_window.geometry("300x200")
    agregar_window.resizable(False, False)
    agregar_window.configure(bg="#F5F5F5")

    nombre_label = ttk.Label(agregar_window, text="Nombre:")
    nombre_label.pack()
    nombre_entry = ttk.Entry(agregar_window)
    nombre_entry.pack()

    precio_label = ttk.Label(agregar_window, text="Precio:")
    precio_label.pack()
    precio_entry = ttk.Entry(agregar_window)
    precio_entry.pack()

    stock_label = ttk.Label(agregar_window, text="Stock:")
    stock_label.pack()
    stock_entry = ttk.Entry(agregar_window)
    stock_entry.pack()

    agregar_button = ttk.Button(agregar_window, text="Agregar", command=agregar)
    agregar_button.pack(pady=10)

# Función para modificar un producto existente
def modificar_producto():
    def modificar():
        id_producto = id_producto_entry.get()

        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
        producto = cursor.fetchone()

        if producto:
            nombre = nombre_entry.get()
            precio = float(precio_entry.get())
            stock = int(stock_entry.get())

            cursor.execute("UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s",
                           (nombre, precio, stock, id_producto))
            db.commit()

            messagebox.showinfo("Producto Modificado", "Producto modificado exitosamente")
        else:
            messagebox.showerror("Error", "El producto no existe")

    modificar_window = tk.Toplevel(window)
    modificar_window.title("Modificar Producto")
    modificar_window.geometry("300x250")
    modificar_window.resizable(False, False)
    modificar_window.configure(bg="#F5F5F5")

    id_producto_label = ttk.Label(modificar_window, text="ID del producto:")
    id_producto_label.pack()
    id_producto_entry = ttk.Entry(modificar_window)
    id_producto_entry.pack()

    nombre_label = ttk.Label(modificar_window, text="Nuevo Nombre:")
    nombre_label.pack()
    nombre_entry = ttk.Entry(modificar_window)
    nombre_entry.pack()

    precio_label = ttk.Label(modificar_window, text="Nuevo Precio:")
    precio_label.pack()
    precio_entry = ttk.Entry(modificar_window)
    precio_entry.pack()

    stock_label = ttk.Label(modificar_window, text="Nuevo Stock:")
    stock_label.pack()
    stock_entry = ttk.Entry(modificar_window)
    stock_entry.pack()

    modificar_button = ttk.Button(modificar_window, text="Modificar", command=modificar)
    modificar_button.pack(pady=10)

# Función para eliminar un producto
def eliminar_producto():
    def eliminar():
        id_producto = id_producto_entry.get()

        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
        producto = cursor.fetchone()

        if producto:
            cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
            db.commit()

            messagebox.showinfo("Producto Eliminado", "Producto eliminado exitosamente")
        else:
            messagebox.showerror("Error", "El producto no existe")

    eliminar_window = tk.Toplevel(window)
    eliminar_window.title("Eliminar Producto")
    eliminar_window.geometry("300x150")
    eliminar_window.resizable(False, False)
    eliminar_window.configure(bg="#F5F5F5")

    id_producto_label = ttk.Label(eliminar_window, text="ID del producto:")
    id_producto_label.pack()
    id_producto_entry = ttk.Entry(eliminar_window)
    id_producto_entry.pack()

    eliminar_button = ttk.Button(eliminar_window, text="Eliminar", command=eliminar)
    eliminar_button.pack(pady=10)




# Función para realizar una compra
def comprar_producto():
    def comprar():
        id_producto = id_producto_entry.get()
        cantidad = int(cantidad_entry.get())
        id_cliente = id_cliente_entry.get()

        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
        producto = cursor.fetchone()

        if producto:
            id_producto, nombre, precio, stock = producto
            precio_total = precio * cantidad

            if cantidad <= stock:
                cursor.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (cantidad, id_producto))
                db.commit()

                cursor.execute("INSERT INTO ventas (id_producto, id_cliente, cantidad, precio_total) VALUES (%s, %s, %s, %s)",
                               (id_producto, id_cliente, cantidad, precio_total))
                db.commit()

                messagebox.showinfo("Compra Realizada", f"Has comprado {cantidad} {nombre}(s) por un total de ${precio_total}")
            else:
                messagebox.showerror("Error", "No hay suficiente stock disponible")
        else:
            messagebox.showerror("Error", "El producto no existe")

    comprar_window = tk.Toplevel(window)
    comprar_window.title("Comprar Producto")
    comprar_window.geometry("300x200")
    comprar_window.resizable(False, False)
    comprar_window.configure(bg="#F5F5F5")

    id_producto_label = ttk.Label(comprar_window, text="ID del producto:")
    id_producto_label.pack()
    id_producto_entry = ttk.Entry(comprar_window)
    id_producto_entry.pack()

    cantidad_label = ttk.Label(comprar_window, text="Cantidad:")
    cantidad_label.pack()
    cantidad_entry = ttk.Entry(comprar_window)
    cantidad_entry.pack()

    id_cliente_label = ttk.Label(comprar_window, text="ID del cliente:")
    id_cliente_label.pack()
    id_cliente_entry = ttk.Entry(comprar_window)
    id_cliente_entry.pack()

    comprar_button = ttk.Button(comprar_window, text="Comprar", command=comprar)
    comprar_button.pack(pady=10)

# Función para el login de administradores
def login_administrador():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT * FROM administradores WHERE username = %s AND password = %s", (username, password))
    administrador = cursor.fetchone()

    if administrador:
        messagebox.showinfo("Login Exitoso", "¡Bienvenido, administrador!")
        admin_window = tk.Toplevel(window)
        admin_window.title("Panel de Administración")
        admin_window.geometry("500x300")
        admin_window.resizable(False, False)
        admin_window.configure(bg="#F5F5F5")

        def show_productos():
            mostrar_productos()

        def add_producto():
            agregar_producto()

        def show_ventas():
            cursor.execute("SELECT v.id, p.nombre, c.nombre, v.cantidad, v.precio_total FROM ventas v JOIN productos p ON v.id_producto = p.id JOIN clientes c ON v.id_cliente = c.id")
            ventas = cursor.fetchall()
            headers = ["ID Venta", "Producto", "Cliente", "Cantidad", "Precio Total"]
            messagebox.showinfo("Ventas Registradas", tabulate(ventas, headers=headers))

        productos_button = ttk.Button(admin_window, text="Mostrar Productos", command=show_productos)
        productos_button.pack(pady=10)

        agregar_button = ttk.Button(admin_window, text="Agregar Producto", command=add_producto)
        agregar_button.pack(pady=10)

        ventas_button = ttk.Button(admin_window, text="Ver Ventas", command=show_ventas)
        ventas_button.pack(pady=10)

        modificar_producto_button = ttk.Button(admin_window, text="Modificar Producto", command=modificar_producto)
        modificar_producto_button.pack(pady=10)

        eliminar_producto_button = ttk.Button(admin_window, text="Eliminar Producto", command=eliminar_producto)
        eliminar_producto_button.pack(pady=10)

    else:
        messagebox.showerror("Error de Login", "Credenciales incorrectas")

# Función para el login de clientes
def login_cliente():
    id_cliente = id_cliente_entry.get()

    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
    cliente = cursor.fetchone()

    if cliente:
        messagebox.showinfo("Login Exitoso", f"Bienvenido, {cliente[1]}!")
        cliente_window = tk.Toplevel(window)
        cliente_window.title("Panel de Cliente")
        cliente_window.geometry("500x250")
        cliente_window.resizable(False, False)
        cliente_window.configure(bg="#F5F5F5")

        def show_productos():
            mostrar_productos()

        def buy_producto():
            comprar_producto()

        productos_button = ttk.Button(cliente_window, text="Mostrar Productos", command=show_productos)
        productos_button.pack(pady=10)

        comprar_button = ttk.Button(cliente_window, text="Comprar Producto", command=buy_producto)
        comprar_button.pack(pady=10)

        historial_compras_button = ttk.Button(cliente_window, text="Historial de Compras", command=historial_compras)
        historial_compras_button.pack(pady=10)
    else:
        messagebox.showerror("Error de Login", "ID de cliente incorrecto")

def registro_cliente():
    def registrar():
        nombre = nombre_entry.get()

        cursor.execute("INSERT INTO clientes (nombre) VALUES (%s)", (nombre,))
        db.commit()

        messagebox.showinfo("Registro Exitoso", f"Registro exitoso. Su ID de cliente es:\n{cursor.lastrowid}")

    registro_window = tk.Toplevel(window)
    registro_window.title("Registro de Cliente")
    registro_window.geometry("300x200")
    registro_window.resizable(False, False)
    registro_window.configure(bg="#F5F5F5")

    nombre_label = ttk.Label(registro_window, text="Nombre:")
    nombre_label.pack()
    nombre_entry = ttk.Entry(registro_window)
    nombre_entry.pack()

    registrar_button = ttk.Button(registro_window, text="Registrar", command=registrar)
    registrar_button.pack(pady=10)


# Función para mostrar el historial de compras de un cliente
def historial_compras():
    def mostrar_historial():
        id_cliente = id_cliente_entry.get()

        cursor.execute(
            "SELECT v.id, p.nombre, v.cantidad, v.precio_total FROM ventas v JOIN productos p ON v.id_producto = p.id WHERE v.id_cliente = %s",
            (id_cliente,))
        historial = cursor.fetchall()

        if historial:
            headers = ["ID Venta", "Producto", "Cantidad", "Precio Total"]
            messagebox.showinfo("Historial de Compras", tabulate(historial, headers=headers))
        else:
            messagebox.showinfo("Historial de Compras", "No hay compras realizadas")

    historial_window = tk.Toplevel(window)
    historial_window.title("Historial de Compras")
    historial_window.geometry("300x150")
    historial_window.resizable(False, False)
    historial_window.configure(bg="#F5F5F5")

    id_cliente_label = ttk.Label(historial_window, text="ID del cliente:")
    id_cliente_label.pack()
    id_cliente_entry = ttk.Entry(historial_window)
    id_cliente_entry.pack()

    mostrar_historial_button = ttk.Button(historial_window, text="Mostrar Historial", command=mostrar_historial)
    mostrar_historial_button.pack(pady=10)

    
# Crear widgets
login_label = ttk.Label(window, text="Bienvenido", font=("Roboto", 15, "bold"))
login_label.pack(pady=20)

admin_frame = ttk.Frame(window, relief=tk.RAISED, padding="20 10 20 10")
admin_frame.pack(pady=10)

username_label = ttk.Label(admin_frame, text="Nombre de usuario:")
username_label.grid(row=0, column=0, sticky=tk.W)
username_entry = ttk.Entry(admin_frame)
username_entry.grid(row=0, column=1, padx=10)

password_label = ttk.Label(admin_frame, text="Contraseña:")
password_label.grid(row=1, column=0, sticky=tk.W)
password_entry = ttk.Entry(admin_frame, show="*")
password_entry.grid(row=1, column=1, padx=10)


login_admin_button = ttk.Button(window, text="Iniciar sesion como administrador", command=login_administrador)
login_admin_button.pack(pady=10)

cliente_frame = ttk.Frame(window, relief=tk.RAISED, padding="20 10 20 10")
cliente_frame.pack(pady=10)

id_cliente_label = ttk.Label(cliente_frame, text="ID de cliente:")
id_cliente_label.grid(row=0, column=0, sticky=tk.W)
id_cliente_entry = ttk.Entry(cliente_frame)
id_cliente_entry.grid(row=0, column=1, padx=10)

login_cliente_button = ttk.Button(window, text="Iniciar sesion como cliente", command=login_cliente)
login_cliente_button.pack(pady=10)

registro_cliente_button = ttk.Button(window, text="Registro de Cliente", command=registro_cliente)
registro_cliente_button.pack(pady=10)



# Ejecutar ventana principal
window.mainloop()

# Cierre de la conexión a la base de datos
cursor.close()
db.close()

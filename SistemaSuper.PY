import mysql.connector
from tabulate import tabulate

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="supermercado"
)
cursor = db.cursor(buffered=True)

# Función para mostrar los productos disponibles
def mostrar_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    headers = ["ID", "Nombre", "Precio", "Stock"]
    print(tabulate(productos, headers=headers))

# Función para mostrar el historial de compras de un cliente
def historial_compras(id_cliente):
    cursor.execute("SELECT v.id, p.nombre, v.cantidad, v.precio_total FROM ventas v JOIN productos p ON v.id_producto = p.id WHERE v.id_cliente = %s", (id_cliente,))
    historial = cursor.fetchall()

    if historial:
        headers = ["ID Venta", "Producto", "Cantidad", "Precio Total"]
        print(tabulate(historial, headers=headers))
    else:
        print("\nNo hay compras realizadas")

# Función para el registro de clientes
def registro_cliente():
    nombre = input("\nIngrese su nombre: ")

    cursor.execute("INSERT INTO clientes (nombre) VALUES (%s)", (nombre,))
    db.commit()

    print("\nRegistro exitoso. Su ID de cliente es:")
    cursor.execute("SELECT LAST_INSERT_ID()")
    id_cliente = cursor.fetchone()[0]
    print(id_cliente)

# Función para modificar un producto existente
def modificar_producto():
    id_producto = input("\nIngrese el ID del producto a modificar: ")

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
    producto = cursor.fetchone()

    if producto:
        print("\nInformación actual del producto:")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Precio: {producto[2]}")
        print(f"Stock: {producto[3]}")

        print("\nIngrese los nuevos datos del producto:")
        nombre = input("Nombre: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))

        cursor.execute("UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s",
                       (nombre, precio, stock, id_producto))
        db.commit()

        print("\nProducto modificado exitosamente")
    else:
        print("\nEl producto no existe")


# Función para borrar un producto existente
def borrar_producto():
    id_producto = input("\nIngrese el ID del producto a borrar: ")

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
    producto = cursor.fetchone()

    if producto:
        print("\nInformación del producto a borrar:")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Precio: {producto[2]}")
        print(f"Stock: {producto[3]}")

        confirmacion = input("\n¿Está seguro de que desea borrar este producto? (s/n): ")

        if confirmacion.lower() == "s":
            cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
            db.commit()
            print("\nProducto borrado exitosamente")
        else:
            print("\nOperación cancelada")
    else:
        print("\nEl producto no existe")


# Función para realizar una compra
def comprar_producto(id_producto, cantidad, id_cliente):
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

            print(f"\nHas comprado {cantidad} {nombre}(s) por un total de ${precio_total}")
        else:
            print("\nNo hay suficiente stock disponible")
    else:
        print("\nEl producto no existe")

# Función para agregar un nuevo producto
def agregar_producto():
    nombre = input("\nIngrese el nombre del nuevo producto: ")
    precio = float(input("Ingrese el precio del nuevo producto: "))
    stock = int(input("Ingrese la cantidad en stock del nuevo producto: "))

    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
    db.commit()

    print("\nProducto agregado exitosamente")

# Función para el login de administradores
def login_administrador():
    username = input("\nIngrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    cursor.execute("SELECT * FROM administradores WHERE username = %s AND password = %s", (username, password))
    administrador = cursor.fetchone()

    if administrador:
        print("\n¡Bienvenido, administrador!")
    while True:
        print("\n--- Panel de Administración ---")
        print("1. Mostrar productos disponibles")
        print("2. Agregar un nuevo producto")
        print("3. Ver ventas")
        print("4. Modificar un producto")
        print("5. Borrar un producto")
        print("6. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            mostrar_productos()
        elif opcion == "2":
            agregar_producto()
        elif opcion == "3":
            mostrar_ventas()
        elif opcion == "4":
            modificar_producto()
        elif opcion == "5":
            borrar_producto()
        elif opcion == "6":
            break
        else:
            print("\nOpción inválida")

# Función para el login de clientes
def login_cliente():
    id_cliente = input("\nIngrese su ID de cliente: ")

    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
    cliente = cursor.fetchone()

    if cliente:
        print("\n¡Bienvenido, cliente!")
        while True:
            print("\n--- Panel de Cliente ---")
            print("1. Mostrar productos disponibles")
            print("2. Comprar un producto")
            print("3. Historial de compras")
            print("4. Salir")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                mostrar_productos()
            elif opcion == "2":
                id_producto = input("\nIngrese el ID del producto a comprar: ")
                cantidad = int(input("Ingrese la cantidad a comprar: "))
                comprar_producto(id_producto, cantidad, id_cliente)
            elif opcion == "3":
                historial_compras(id_cliente)
            elif opcion == "4":
                break
            else:
                print("\nOpción inválida")
    else:
        print("\nID de cliente incorrecto")


# Función para mostrar las ventas registradas
def mostrar_ventas():
    cursor.execute("SELECT v.id, p.nombre, c.nombre, v.cantidad, v.precio_total FROM ventas v JOIN productos p ON v.id_producto = p.id JOIN clientes c ON v.id_cliente = c.id")
    ventas = cursor.fetchall()
    headers = ["ID Venta", "Producto", "Cliente", "Cantidad", "Precio Total"]
    print(tabulate(ventas, headers=headers))

# Menú principal
while True:
    print("\n--- Punto de Compra y Venta ---")
    print("1. Administrador")
    print("2. Cliente")
    print("3. Registro de Cliente")
    print("4. Salir")
    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        login_administrador()
    elif opcion == "2":
        login_cliente()
    elif opcion == "3":
        registro_cliente()
    elif opcion == "4":
        break
    else:
        print("\nOpción inválida")

# Cierre de la conexión a la base de datos
cursor.close()
db.close()

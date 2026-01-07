class Usuario:
    def __init__(self, full_name, username, password, id=None):
        self.id = id
        self.full_name = full_name
        self.username = username
        self.password = password

    @staticmethod
    def from_row(row):
        # id, full_name, username, password
        return Usuario(row[1], row[2], row[3], id=row[0])

class Categoria:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    @staticmethod
    def from_row(row):
        return Categoria(row[0], row[1])

class Producto:
    def __init__(self, codigo, nombre, categoria_id, proveedor_id, quantity, price):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria_id = int(categoria_id)
        self.proveedor_id = int(proveedor_id)
        self.cantidad = int(quantity)
        self.precio = float(price)

    @staticmethod
    def from_row(row):
        # codigo, nombre, cat_id, prov_id, qty, price
        return Producto(row[0], row[1], row[2], row[3], row[4], row[5])

class Cliente:
    def __init__(self, codigo, cedula, nombre, provincia, telefono, correo):
        self.codigo = codigo
        self.cedula = cedula
        self.nombre = nombre
        self.provincia = provincia
        self.telefono = telefono
        self.correo = correo

    @staticmethod
    def from_row(row):
        return Cliente(row[0], row[1], row[2], row[3], row[4], row[5])

class Proveedor:
    def __init__(self, codigo, cedula, nombre, telefono, correo):
        self.codigo = codigo
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    @staticmethod
    def from_row(row):
        return Proveedor(row[0], row[1], row[2], row[3], row[4])

class OrdenCompra:
    def __init__(self, codigo, proveedor_id, fecha, total):
        self.codigo = codigo
        self.proveedor_id = proveedor_id
        self.fecha = fecha
        self.total = float(total)

    @staticmethod
    def from_row(row):
        return OrdenCompra(row[0], row[1], row[2], row[3])

class DetalleOrden:
    def __init__(self, id, orden_id, producto_id, cantidad, precio_unitario):
        self.id = id
        self.orden_id = orden_id
        self.producto_id = producto_id
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)

    @staticmethod
    def from_row(row):
        # id, orden_id, prod_id, qty, price
        return DetalleOrden(row[0], row[1], row[2], row[3], row[4])

class Factura:
    def __init__(self, codigo, cliente_id, fecha, total):
        self.codigo = codigo
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.total = float(total)

    @staticmethod
    def from_row(row):
        return Factura(row[0], row[1], row[2], row[3])

class DetalleFactura:
    def __init__(self, id, factura_id, producto_id, cantidad, precio_unitario):
        self.id = id
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)

    @staticmethod
    def from_row(row):
        return DetalleFactura(row[0], row[1], row[2], row[3], row[4])

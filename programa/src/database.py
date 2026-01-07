import sqlite3
import os
from src.logger import log_info, log_error

DB_NAME = "data/sistema_ventas.db"

class DatabaseManager:
    @staticmethod
    def get_connection():
        if not os.path.exists("data"):
            os.makedirs("data")
        return sqlite3.connect(DB_NAME)

    @staticmethod
    def initialize_db():
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            # Users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            # Categories
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
                )
            ''')
            
            # Providers
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proveedores (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    cedula TEXT,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    correo TEXT
                )
            ''')
            
            # Products
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    categoria_id INTEGER,
                    proveedor_id INTEGER,
                    cantidad INTEGER DEFAULT 0,
                    precio REAL,
                    FOREIGN KEY(categoria_id) REFERENCES categorias(codigo),
                    FOREIGN KEY(proveedor_id) REFERENCES proveedores(codigo)
                )
            ''')
            
            # Clients
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    cedula TEXT,
                    nombre TEXT NOT NULL,
                    provincia TEXT,
                    telefono TEXT,
                    correo TEXT
                )
            ''')
            
            # Orders
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ordenes (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    proveedor_id INTEGER,
                    fecha TEXT,
                    total REAL,
                    FOREIGN KEY(proveedor_id) REFERENCES proveedores(codigo)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalle_ordenes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    orden_id INTEGER,
                    producto_id INTEGER,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    FOREIGN KEY(orden_id) REFERENCES ordenes(codigo),
                    FOREIGN KEY(producto_id) REFERENCES productos(codigo)
                )
            ''')
            
            # Invoices
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facturas (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    fecha TEXT,
                    total REAL,
                    FOREIGN KEY(cliente_id) REFERENCES clientes(codigo)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalle_facturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    factura_id INTEGER,
                    producto_id INTEGER,
                    cantidad INTEGER,
                    precio_unitario REAL,
                    FOREIGN KEY(factura_id) REFERENCES facturas(codigo),
                    FOREIGN KEY(producto_id) REFERENCES productos(codigo)
                )
            ''')
            
            # Check for default user
            cursor.execute("SELECT * FROM usuarios WHERE username='admin'")
            if not cursor.fetchone():
                cursor.execute("INSERT INTO usuarios (full_name, username, password) VALUES (?, ?, ?)",
                               ("Administrador", "admin", "admin"))
                log_info("Default admin user created.")
                
            conn.commit()
            conn.close()
            log_info("Database initialized successfully.")
            
        except Exception as e:
            log_error("Failed to init database", e)

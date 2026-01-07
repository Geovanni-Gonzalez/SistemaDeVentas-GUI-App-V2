from src.database import DatabaseManager
from src.models import Producto, Factura, DetalleFactura, Cliente
from datetime import datetime, timedelta
import random

def seed_simulation():
    DatabaseManager.initialize_db()
    conn = DatabaseManager.get_connection()
    cursor = conn.cursor()
    
    # 1. Create a "Hot Product"
    cursor.execute("INSERT INTO categorias (nombre) VALUES ('Electrónica')")
    cat_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO proveedores (nombre) VALUES ('TechDistributor')")
    prov_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO productos (nombre, categoria_id, proveedor_id, cantidad, precio) VALUES (?, ?, ?, ?, ?)",
                   ("SmartWatch AI", cat_id, prov_id, 10, 15000))
    prod_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO clientes (nombre) VALUES ('Cliente Demo')")
    cli_id = cursor.lastrowid
    
    print(f"Features Product Created: SmartWatch AI (ID: {prod_id}) - Stock: 10")
    
    # 2. Simulate Sales over past 5 days (2 per day)
    # 10 units stock. Selling 2/day -> 5 days left. AI should predict ~5 days.
    
    for i in range(5, 0, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%d/%m/%Y")
        
        # Create Invoice
        cursor.execute("INSERT INTO facturas (cliente_id, fecha, total) VALUES (?, ?, ?)", (cli_id, date, 30000))
        fact_id = cursor.lastrowid
        
        # Create Detail (Sold 2)
        cursor.execute("INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                       (fact_id, prod_id, 2, 15000))
                       
    conn.commit()
    conn.close()
    print("Simulation Data Seeded!")

if __name__ == "__main__":
    seed_simulation()

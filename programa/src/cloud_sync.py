import csv
import os
import json
from datetime import datetime
from src.database import DatabaseManager
from src.logger import log_info

class CloudSync:
    def __init__(self):
        self.sync_folder = "cloud_sync"
        if not os.path.exists(self.sync_folder):
            os.makedirs(self.sync_folder)

    def sync_sales_to_cloud(self):
        """
        Simulates syncing Daily Sales to Google Sheets by creating formatted CSVs
        that would be picked up by a cloud agent.
        """
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime("%d/%m/%Y")
        
        try:
            # Query Daily Sales
            query = '''
                SELECT f.codigo, c.nombre, f.total 
                FROM facturas f
                JOIN clientes c ON f.cliente_id = c.codigo
                WHERE f.fecha = ?
            '''
            # Note: Date format in DB is DD/MM/YYYY string based on previous inserts
            cursor.execute(query, (today,))
            rows = cursor.fetchall()
            
            # Export to CSV (Google Sheets Format)
            filename = f"{self.sync_folder}/sales_{datetime.now().strftime('%Y-%m-%d')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID Factura", "Cliente", "Total", "Sincronizado En"])
                for row in rows:
                    writer.writerow(list(row) + [datetime.now().isoformat()])
            
            log_info(f"Cloud Sync successful: {filename}")
            return True, f"Datos subidos a la Nube ({len(rows)} ventas hoy)\nArchivo: {filename}"
            
        except Exception as e:
            log_info(f"Cloud Sync failed: {e}")
            return False, str(e)
        finally:
            conn.close()

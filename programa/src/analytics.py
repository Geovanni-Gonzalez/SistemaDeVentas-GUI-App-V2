import sqlite3
from src.database import DatabaseManager
from src.logger import log_error

class SalesPredictor:
    def __init__(self):
        self.conn = DatabaseManager.get_connection()

    def get_sales_history(self, product_id):
        """ Fetch daily sales quantity for a product """
        try:
            cursor = self.conn.cursor()
            # Join items with invoice to get date
            # We treat date as ordinal (simple day count) for regression if needed, 
            # but for simple burn rate we just need avg daily sales over active period.
            
            # Sum quantity per day
            query = '''
                SELECT f.fecha, SUM(d.cantidad)
                FROM detalle_facturas d
                JOIN facturas f ON d.factura_id = f.codigo
                WHERE d.producto_id = ?
                GROUP BY f.fecha
                ORDER BY f.fecha ASC
            '''
            cursor.execute(query, (product_id,))
            return cursor.fetchall() # [(date_str, qty), ...]
        except Exception as e:
            log_error("Error fetching history", e)
            return []

    def predict_days_remaining(self, product_id, current_stock):
        """ 
        Calculate burn rate using simple linear average (Total Sold / Days Active).
        Linear Regression Logic:
        Slope (m) = Rate of sales per day.
        Days Remaining = Current Stock / m
        """
        history = self.get_sales_history(product_id)
        if not history: return None # No data to predict
        
        # Determine timespan
        # Date format DD/MM/YYYY. Need simple conversion.
        from datetime import datetime
        
        try:
            dates = [datetime.strptime(row[0], "%d/%m/%Y") for row in history]
            total_sold = sum([row[1] for row in history])
            
            if not dates: return None
            
            first_sale = min(dates)
            last_sale = max(dates) # Or today
            
            days_span = (datetime.now() - first_sale).days
            if days_span == 0: days_span = 1 # Avoid div by zero
            
            burn_rate = total_sold / days_span # units per day
            
            if burn_rate <= 0: return 999 # No sales velocity
            
            days_left = current_stock / burn_rate
            return int(days_left)
            
        except Exception as e:
            log_error(f"Prediction error for {product_id}", e)
            return None

    def close(self):
        self.conn.close()

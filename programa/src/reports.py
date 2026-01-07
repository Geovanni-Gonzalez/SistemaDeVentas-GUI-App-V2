from fpdf import FPDF
import os
from datetime import datetime

class PDFGenerator(FPDF):
    def header(self):
        # Logo placeholder or Company Name
        self.set_font('Arial', 'B', 20)
        self.set_text_color(52, 152, 219) # Accent Color
        self.cell(0, 10, 'SISTEMA DE VENTAS', 0, 1, 'L')
        
        self.set_font('Arial', 'I', 10)
        self.set_text_color(128)
        self.cell(0, 5, 'Soluciones Tecnologicas S.A.', 0, 1, 'L')
        self.cell(0, 5, 'San Jose, Costa Rica | Tel: +506 2222-5555', 0, 1, 'L')
        self.ln(10)
        
        # Line break
        self.set_draw_color(52, 152, 219)
        self.set_line_width(1)
        self.line(10, 35, 200, 35)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def generate_invoice_pdf(self, factura, cliente, items):
        self.add_page()
        
        # Title
        self.set_font('Arial', 'B', 16)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, f'FACTURA DE VENTA #{factura.codigo}', 0, 1, 'R')
        self.ln(5)
        
        # Client Info Box
        self.set_fill_color(240, 240, 240)
        self.set_draw_color(200)
        self.set_line_width(0.2)
        
        start_y = self.get_y()
        self.rect(10, start_y, 190, 30, 'FD')
        
        self.set_xy(15, start_y + 5)
        self.set_font('Arial', 'B', 11)
        self.cell(30, 6, 'Cliente:', 0, 0)
        self.set_font('Arial', '', 11)
        self.cell(80, 6, cliente.nombre, 0, 1)
        
        self.set_x(15)
        self.set_font('Arial', 'B', 11)
        self.cell(30, 6, 'Telefono:', 0, 0)
        self.set_font('Arial', '', 11)
        self.cell(80, 6, cliente.telefono, 0, 1)
        
        self.set_x(15)
        self.set_font('Arial', 'B', 11)
        self.cell(30, 6, 'Fecha:', 0, 0)
        self.set_font('Arial', '', 11)
        self.cell(80, 6, factura.fecha, 0, 1)
        
        self.ln(15)
        
        # Table Header
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255)
        self.set_font('Arial', 'B', 11)
        self.cell(20, 10, "Cant.", 1, 0, 'C', 1)
        self.cell(100, 10, "Producto", 1, 0, 'C', 1)
        self.cell(35, 10, "Precio Unit", 1, 0, 'C', 1)
        self.cell(35, 10, "Subtotal", 1, 1, 'C', 1)
        
        # Table Body
        self.set_font('Arial', '', 10)
        self.set_text_color(0)
        self.set_fill_color(245, 245, 245)
        
        total = 0
        fill = False
        for item in items:
            prod_name = item['prod'].nombre
            qty = item['qty']
            price = item['price']
            sub = qty * price
            total += sub
            
            self.cell(20, 10, str(qty), 'LR', 0, 'C', fill)
            self.cell(100, 10, prod_name, 'LR', 0, 'L', fill)
            self.cell(35, 10, f"{price:,.2f}", 'LR', 0, 'R', fill)
            self.cell(35, 10, f"{sub:,.2f}", 'LR', 1, 'R', fill)
            fill = not fill
            
        self.cell(190, 0, '', 'T', 1) # Closing line
        
        # Totals
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255)
        
        # Total Box
        self.set_x(135)
        self.cell(30, 10, "TOTAL:", 1, 0, 'R', 1)
        self.set_text_color(0)
        self.cell(35, 10, f"{total:,.2f}", 1, 1, 'R')
        
        if not os.path.exists("reportes"):
            os.makedirs("reportes")
        filename = f"reportes/Factura_{factura.codigo}.pdf"
        self.output(filename)
        return filename

    def generate_list_report(self, title, headers, data, filename):
        self.add_page()
        
        self.set_font('Arial', 'B', 18)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)
        
        # Determine col widths
        n_cols = len(headers)
        w = 190 / n_cols
        
        # Header
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255)
        self.set_font('Arial', 'B', 11)
        for h in headers:
            self.cell(w, 10, h, 1, 0, 'C', 1)
        self.ln()
        
        # Rows
        self.set_font('Arial', '', 10)
        self.set_text_color(0)
        self.set_fill_color(245, 245, 245)
        
        fill = False
        for row in data:
            for item in row:
                self.cell(w, 10, str(item), 1, 0, 'C', fill)
            self.ln()
            fill = not fill
            
        if not os.path.exists("reportes"):
             os.makedirs("reportes")
        path = f"reportes/{filename}.pdf"
        self.output(path)
        return path

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.repository import Repository
from src.models import Cliente, Producto, Factura, DetalleFactura
from src.ui.theme import Theme

class BillingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Facturación (Venta)")
        self.geometry("800x600")
        Theme.apply_styles(self)
        
        self.repo_cli = Repository("clientes")
        self.repo_prod = Repository("productos")
        self.repo_fact = Repository("facturas")
        self.repo_detalle = Repository("detalle_facturas")
        
        self.clientes = self.repo_cli.load_all(Cliente.from_row)
        self.productos = self.repo_prod.load_all(Producto.from_row)
        
        self.cart = [] 
        
        # UI Layout
        # 1. Header (Client Select)
        frame_head = tk.Frame(self)
        frame_head.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_head, text="Cliente:").pack(side='left')
        self.combo_cli = ttk.Combobox(frame_head, values=[f"{c.codigo} - {c.nombre}" for c in self.clientes])
        self.combo_cli.pack(side='left', fill='x', expand=True, padx=5)
        
        # Product Selection
        # The original code used 'frame_prod' as a LabelFrame.
        # The instruction's code edit uses 'prod_frame' and references 'main_frame' which is not defined.
        # I will adapt the instruction's code to use 'self' as the parent for 'prod_frame'
        # and use the existing theme attributes where applicable, or default if not specified in Theme.
        prod_frame = tk.LabelFrame(self, text="Producto", padx=10, pady=10, bg=Theme.BG_MAIN, fg=Theme.PRIMARY)
        prod_frame.pack(fill='x', pady=5)
        
        tk.Label(prod_frame, text="Buscar:", bg=Theme.BG_MAIN, fg=Theme.TEXT_LIGHT).grid(row=0, column=0, padx=5)
        
        self.prod_combo = ttk.Combobox(prod_frame, values=[f"{p.codigo} - {p.nombre}" for p in self.productos], width=30)
        self.prod_combo.grid(row=0, column=1, padx=5)
        # The instruction includes a bind to self.update_price, which is not in the original code.
        # To maintain syntactical correctness and avoid errors, I will add a placeholder method for update_price.
        self.prod_combo.bind("<<ComboboxSelected>>", self.update_price)
        
        # SCAN BUTTON
        tk.Button(prod_frame, text="📷 Escanear", command=self.scan_product, bg=Theme.ACCENT, fg=Theme.BG_DARK).grid(row=0, column=2, padx=5)
        
        tk.Label(prod_frame, text="Cantidad:", bg=Theme.BG_MAIN, fg=Theme.TEXT_LIGHT).grid(row=0, column=3, padx=5)
        self.qty_entry = ttk.Entry(prod_frame, width=5)
        self.qty_entry.grid(row=0, column=4, padx=5)
        
        self.price_label = tk.Label(prod_frame, text="Precio: $0.00", bg=Theme.BG_MAIN, fg=Theme.TEXT_MUTED)
        self.price_label.grid(row=0, column=5, padx=10)
        
        ttk.Button(prod_frame, text="Agregar", command=self.add_to_cart).grid(row=0, column=6, padx=10)
        
        # 3. List
        self.tree = ttk.Treeview(self, columns=("ID", "Producto", "Cant", "Precio", "Subtotal"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 4. Footer
        frame_foot = tk.Frame(self)
        frame_foot.pack(fill='x', padx=10, pady=10)
        
        self.lbl_total = tk.Label(frame_foot, text="Total: 0.00", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side='right')
        
        tk.Button(frame_foot, text="Procesar Factura", bg="#2196f3", fg="white", command=self.save_invoice).pack(side='left')

    def add_to_cart(self):
        prod_val = self.prod_combo.get()
        if not prod_val: return
        
        pid = int(prod_val.split(' - ')[0])
        prod_obj = next((p for p in self.productos if p.codigo == pid), None)
        
        try:
            qty = int(self.entry_qty.get())
            if qty <= 0: raise ValueError
            if qty > prod_obj.cantidad:
                messagebox.showwarning("Stock Insuficiente", f"Solo hay {prod_obj.cantidad} unidades disponibles.")
                return
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return
            
        self.cart.append({'prod': prod_obj, 'qty': qty, 'price': prod_obj.precio})
        self.refresh_cart()

    def refresh_cart(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total = 0
        for item in self.cart:
            sub = item['qty'] * item['price']
            total += sub
            self.tree.insert('', 'end', values=(item['prod'].codigo, item['prod'].nombre, item['qty'], item['price'], sub))
            
        self.lbl_total.config(text=f"Total: {total:.2f}")

    def update_price(self, event):
        val = self.prod_combo.get()
        if not val: return
        
        pid = int(val.split(' - ')[0])
        prod = next((p for p in self.productos if p.codigo == pid), None)
        
        if prod:
            self.price_label.config(text=f"Precio: ${prod.precio:.2f}")
            self.current_prod = prod

    def save_invoice(self):
        cli_val = self.combo_cli.get()
        if not cli_val or not self.cart:
            messagebox.showerror("Error", "Seleccione cliente y agregue productos")
            return
            
        cli_id = int(cli_val.split(' - ')[0])
        
        # Validate stock again in case of duplicates/race condition (simplified)
        for item in self.cart:
             if item['prod'].cantidad < item['qty']:
                 messagebox.showerror("Error", f"Stock insuficiente para {item['prod'].nombre}")
                 return
        
        total = sum([i['qty'] * i['price'] for i in self.cart])
        date_str = datetime.now().strftime("%d/%m/%Y")
        
        # Create Invoice (SQL return ID)
        fact = Factura(0, cli_id, date_str, total)
        new_id = self.repo_fact.create(fact)
        fact.codigo = new_id 
        
        # Save Details and Update Stock
        for item in self.cart:
            det = DetalleFactura(new_id, item['prod'].codigo, item['qty'], item['price'])
            self.repo_detalle.create(det)
            
            # Update individual product stock in DB
            item['prod'].cantidad -= item['qty']
            self.repo_prod.update(item['prod'])
          # Generate PDF
        try:
            from src.reports import PDFGenerator
            gen = PDFGenerator()
            client_obj = next(c for c in self.clientes if c.codigo == cli_id)
            fpath = gen.generate_invoice_pdf(fact, client_obj, self.cart)
            msg = f"Factura #{new_id} generada.\nReporte: {fpath}"
            
            # --- EMAIL ---
            from src.emailer import EmailService
            emailer = EmailService()
            if hasattr(client_obj, 'correo') and client_obj.correo:
                result = emailer.send_invoice(client_obj.correo, fpath, new_id)
                if result: msg += "\n✉ Correo enviado."

            # --- WHATSAPP ---
            if hasattr(client_obj, 'telefono') and client_obj.telefono:
                from src.whatsapp_client import WhatsAppClient
                wa = WhatsAppClient()
                # Ask user if they want to send WA
                if messagebox.askyesno("WhatsApp", "¿Enviar comprobante por WhatsApp?"):
                    wa.send_invoice_link(client_obj.telefono, new_id)
                    msg += "\n📱 WhatsApp abierto."
                
        except Exception as e:
            msg = f"Factura #{new_id} generada. Error Post-Proceso: {str(e)}"
        
        messagebox.showinfo("Éxito", msg)
        self.destroy()

    def add_product(self):
        # Modified to support Scanning
        pass # Replaced by logic in __init__ binding or button

    def scan_product(self):
        try:
            from src.scanner import BarcodeScanner
            scanner = BarcodeScanner()
            code = scanner.scan_single() # May return None or string
            
            if code:
                # Find product by code (Assuming code map to ID or Name for now, or new 'codigo_barras' field)
                # Since we don't have 'codigo_barras' column, we assume ID or Name match.
                # Let's try to match ID first.
                prod = next((p for p in self.productos if str(p.codigo) == code or p.nombre == code), None)
                
                if prod:
                    self.current_prod = prod
                    self.prod_combo.set(f"{prod.codigo} - {prod.nombre}")
                    self.update_price(None) 
                    self.qty_entry.focus()
                else:
                    messagebox.showwarning("Escáner", f"Producto no encontrado: {code}")
        except Exception as e:
            messagebox.showerror("Error Escáner", str(e))

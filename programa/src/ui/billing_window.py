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
        
        # 2. Product Entry
        frame_prod = tk.LabelFrame(self, text="Agregar Producto")
        frame_prod.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_prod, text="Producto:").grid(row=0, column=0)
        self.combo_prod = ttk.Combobox(frame_prod, values=[f"{p.codigo} - {p.nombre} (Stock: {p.cantidad})" for p in self.productos])
        self.combo_prod.grid(row=0, column=1, sticky='ew')
        
        tk.Label(frame_prod, text="Cantidad:").grid(row=0, column=2)
        self.entry_qty = tk.Entry(frame_prod, width=10)
        self.entry_qty.grid(row=0, column=3)
        
        tk.Button(frame_prod, text="Agregar", command=self.add_to_cart).grid(row=0, column=4, padx=5)
        
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
        prod_val = self.combo_prod.get()
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
            
        try:
            from src.reports import PDFGenerator
            gen = PDFGenerator()
            client_obj = next(c for c in self.clientes if c.codigo == cli_id)
            fpath = gen.generate_invoice_pdf(fact, client_obj, self.cart)
            msg = f"Factura #{new_id} generada (SQL).\nReporte: {fpath}"
            
            # Send Email
            from src.emailer import EmailService
            emailer = EmailService()
            if hasattr(client_obj, 'correo') and client_obj.correo:
                result = emailer.send_invoice(client_obj.correo, fpath, new_id)
                if result: msg += "\nCorreo enviado exitosamente."
                
        except Exception as e:
            msg = f"Factura #{new_id} generada. Error Post-Proceso: {str(e)}"
        
        messagebox.showinfo("Éxito", msg)
        self.destroy()

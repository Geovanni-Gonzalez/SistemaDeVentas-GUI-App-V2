import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.repository import Repository
from src.models import Proveedor, Producto, OrdenCompra, DetalleOrden
from src.ui.theme import Theme

class OrdersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Orden de Compra")
        self.geometry("800x600")
        Theme.apply_styles(self)
        
        self.repo_prov = Repository("proveedores")
        self.repo_prod = Repository("productos")
        self.repo_orden = Repository("ordenes")
        self.repo_detalle = Repository("detalle_ordenes")
        
        self.proveedores = self.repo_prov.load_all(Proveedor.from_row)
        self.productos = self.repo_prod.load_all(Producto.from_row)
        
        self.cart = [] # List of (product_obj, qty, cost)
        
        # UI Layout
        # 1. Header (Provider Select)
        frame_head = tk.Frame(self)
        frame_head.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_head, text="Proveedor:").pack(side='left')
        self.combo_prov = ttk.Combobox(frame_head, values=[f"{p.codigo} - {p.nombre}" for p in self.proveedores])
        self.combo_prov.pack(side='left', fill='x', expand=True, padx=5)
        
        # 2. Product Entry
        frame_prod = tk.LabelFrame(self, text="Agregar Producto")
        frame_prod.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame_prod, text="Producto:").grid(row=0, column=0)
        self.combo_prod = ttk.Combobox(frame_prod, values=[f"{p.codigo} - {p.nombre}" for p in self.productos])
        self.combo_prod.grid(row=0, column=1, sticky='ew')
        
        tk.Label(frame_prod, text="Cantidad:").grid(row=0, column=2)
        self.entry_qty = tk.Entry(frame_prod, width=10)
        self.entry_qty.grid(row=0, column=3)
        
        tk.Label(frame_prod, text="Costo Unit:").grid(row=0, column=4)
        self.entry_cost = tk.Entry(frame_prod, width=10)
        self.entry_cost.grid(row=0, column=5)
        
        tk.Button(frame_prod, text="Agregar", command=self.add_to_cart).grid(row=0, column=6, padx=5)
        
        # 3. List
        self.tree = ttk.Treeview(self, columns=("ID", "Producto", "Cant", "Costo", "Subtotal"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 4. Footer
        frame_foot = tk.Frame(self)
        frame_foot.pack(fill='x', padx=10, pady=10)
        
        self.lbl_total = tk.Label(frame_foot, text="Total: 0.00", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side='right')
        
        tk.Button(frame_foot, text="Guardar Orden", bg="#4caf50", fg="white", command=self.save_order).pack(side='left')

    def add_to_cart(self):
        prod_val = self.combo_prod.get()
        if not prod_val: return
        
        pid = int(prod_val.split(' - ')[0])
        prod_obj = next((p for p in self.productos if p.codigo == pid), None)
        
        try:
            qty = int(self.entry_qty.get())
            cost = float(self.entry_cost.get())
            if qty <= 0 or cost < 0: raise ValueError
        except:
            messagebox.showerror("Error", "Bolsa de valores inválidos")
            return
            
        self.cart.append({'prod': prod_obj, 'qty': qty, 'cost': cost})
        self.refresh_cart()

    def refresh_cart(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total = 0
        for item in self.cart:
            sub = item['qty'] * item['cost']
            total += sub
            self.tree.insert('', 'end', values=(item['prod'].codigo, item['prod'].nombre, item['qty'], item['cost'], sub))
            
        self.lbl_total.config(text=f"Total: {total:.2f}")

    def save_order(self):
        prov_val = self.combo_prov.get()
        if not prov_val or not self.cart:
            messagebox.showerror("Error", "Seleccione proveedor y agregue productos")
            return
            
        prov_id = int(prov_val.split(' - ')[0])
        
        total = sum([i['qty'] * i['cost'] for i in self.cart])
        date_str = datetime.now().strftime("%d/%m/%Y")
        
        # Create Order (Code 0, let DB assign)
        orden = OrdenCompra(0, prov_id, date_str, total)
        # Repository Create Returns the new ID
        new_id = self.repo_orden.create(orden)
        
        # Save Details and Update Stock
        for item in self.cart:
            det = DetalleOrden(new_id, item['prod'].codigo, item['qty'], item['cost'])
            self.repo_detalle.create(det)
            
            # Update Stock via Repo Update
            item['prod'].cantidad += item['qty']
            self.repo_prod.update(item['prod'])
            
        messagebox.showinfo("Éxito", f"Orden #{new_id} guardada (SQL). Inventario actualizado.")
        self.destroy()

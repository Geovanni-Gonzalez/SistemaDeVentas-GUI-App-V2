import tkinter as tk
import os
from tkinter import ttk, messagebox
from src.repository import Repository
from src.models import Categoria, Producto, Cliente, Proveedor
from src.ui.theme import Theme

class GenericCrudFrame(ttk.Frame):
    def __init__(self, parent, model_class, filename, fields):
        super().__init__(parent)
        self.model_class = model_class
        self.repo = Repository(filename)
        self.fields = fields # List of (label, attrib_name)
        self.entries = {}
        self.model_name = model_class.__name__
        
        # 1. Top Bar: Search and Actions
        top_bar = ttk.Frame(self)
        top_bar.pack(side='top', fill='x', pady=10)
        
        ttk.Label(top_bar, text="Buscar:").pack(side='left', padx=(10, 5))
        self.entry_search = ttk.Entry(top_bar)
        self.entry_search.pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(top_bar, text="Filtrar", command=self.perform_search).pack(side='left', padx=10)
        
        # 2. Form Area (Left or Top) - Let's use Sidebar
        main_content = ttk.Frame(self)
        main_content.pack(fill='both', expand=True, padx=10, pady=5)
        
        form_frame = ttk.LabelFrame(main_content, text="Detalle de Registro", padding=15)
        form_frame.pack(side='left', fill='y', padx=(0, 10))
        
        for i, (lbl, attr) in enumerate(fields):
            ttk.Label(form_frame, text=lbl).pack(anchor='w', pady=(10,0))
            entry = ttk.Entry(form_frame)
            if attr == 'codigo':
                entry.config(state='disabled') 
            entry.pack(fill='x', pady=5)
            self.entries[attr] = entry
            
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill='x', pady=20)
        
        ttk.Button(btn_frame, text="Guardar", command=self.save_item).pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear_form).pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Eliminar", style="Danger.TButton", command=self.delete_item).pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Exportar CSV", command=self.export_csv).pack(fill='x', pady=(20, 5))
        
        # 3. Treeview Area
        tree_frame = ttk.Frame(main_content)
        tree_frame.pack(side='right', fill='both', expand=True)
        
        cols = [attr for _, attr in fields]
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        for lbl, attr in fields:
            self.tree.heading(attr, text=lbl)
            self.tree.column(attr, width=100)
            
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        
        scroll.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        self.refresh_list()

    def export_csv(self):
        try:
            import csv
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                initialdir=".",
                title="Guardar CSV",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                defaultextension=".csv"
            )
            
            if not filename:
                return
                
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow([lbl for lbl, _ in self.fields])
                
                # Data
                for item in self.tree.get_children():
                    vals = self.tree.item(item)['values']
                    writer.writerow(vals)
                    
            messagebox.showinfo("Éxito", "Datos exportados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al exportar: {e}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.config(state='normal')
            entry.delete(0, 'end')
        self.entries['codigo'].config(state='disabled')
        self.tree.selection_remove(self.tree.selection())

    def get_next_id(self, items):
        if not items: return 1
        return max([int(getattr(i, 'codigo')) for i in items]) + 1

    def refresh_list(self, filter_text=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.items = self.repo.load_all(self.model_class.from_row)
        
        for item in self.items:
            matches = True
            if filter_text:
                # Basic case-insensitive search in all fields
                matches = False
                for _, attr in self.fields:
                    val = str(getattr(item, attr)).lower()
                    if filter_text.lower() in val:
                        matches = True
                        break
            
            if matches:
                values = [getattr(item, attr) for _, attr in self.fields]
                self.tree.insert('', 'end', values=values)

    def perform_search(self):
        txt = self.entry_search.get()
        self.refresh_list(txt)

    def save_item(self):
        data = {}
        for _, attr in self.fields:
            if attr == 'codigo': continue
            data[attr] = self.entries[attr].get()

        selected = self.tree.selection()
        if selected:
            # Update
            cur_id = int(self.tree.item(selected[0], 'values')[0])
            for i, item in enumerate(self.items):
                if int(item.codigo) == cur_id:
                     # Update object attributes
                     for k, v in data.items():
                         setattr(item, k, v)
                     # Call Repo Update
                     self.repo.update(item)
                     break
            messagebox.showinfo("Success", "Registro actualizado")
        else:
            # Create
            # ID is auto by DB, we pass None or 0 and let DB handle it?
            # My models expect ID in constructor. 
            # I can pass 0 and then reload.
            new_id = 0 
            if self.model_class == Categoria:
                obj = Categoria(new_id, data['nombre'])
            elif self.model_class == Producto:
                 obj = Producto(new_id, data['nombre'], data['categoria_id'], data['proveedor_id'], 0, data['precio'])
            elif self.model_class == Cliente:
                 obj = Cliente(new_id, data['cedula'], data['nombre'], data['provincia'], data['telefono'], data['correo'])
            elif self.model_class == Proveedor:
                 obj = Proveedor(new_id, data['cedula'], data['nombre'], data['telefono'], data['correo'])
            
            self.repo.create(obj)
            messagebox.showinfo("Success", "Registro creado")

        self.clear_form()
        self.refresh_list()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected: return
        
        cur_id = int(self.tree.item(selected[0], 'values')[0])
        
        # Validation Logic (Requirement: Constraints)
        if not self.validate_deletion(cur_id):
            return

        confirm = messagebox.askyesno("Confirmar", "¿Eliminar registro seleccionado?")
        if not confirm: return
        
        self.repo.delete(cur_id)
        self.clear_form()
        self.refresh_list()

    def validate_deletion(self, _id):
        # Implement specific logic based on model
        from src.models import DetalleFactura, DetalleOrden, Factura, OrdenCompra
        
        if self.model_class == Categoria:
            # Check products
            repo_prod = Repository("productos") # SQL
            prods = repo_prod.load_all(Producto.from_row)
            if any(p.categoria_id == _id for p in prods):
                messagebox.showerror("Error", "No se puede eliminar: Categoría tiene productos asociados.")
                return False
                
        elif self.model_class == Producto:
            # Check invoices via DetalleFactura table
            repo_det = Repository("detalle_facturas")
            alles = repo_det.load_all(DetalleFactura.from_row) 
            # In SQL usually we do proper relational check, but this works for now
            if any(d.producto_id == _id for d in alles):
                 messagebox.showerror("Error", "No se puede eliminar: Producto ha sido facturado.")
                 return False
                        
        elif self.model_class == Cliente:
            # Check invoices 
            repo_fact = Repository("facturas")
            facts = repo_fact.load_all(Factura.from_row)
            if any(f.cliente_id == _id for f in facts):
                 messagebox.showerror("Error", "No se puede eliminar: Cliente tiene facturas.")
                 return False

        elif self.model_class == Proveedor:
            # Check orders
            repo_ord = Repository("ordenes")
            orders = repo_ord.load_all(OrdenCompra.from_row)
            if any(o.proveedor_id == _id for o in orders):
                 messagebox.showerror("Error", "No se puede eliminar: Proveedor tiene órdenes de compra.")
                 return False
                         
        return True

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0], 'values')
        
        for i, (_, attr) in enumerate(self.fields):
            entry = self.entries[attr]
            entry.config(state='normal')
            entry.delete(0, 'end')
            entry.insert(0, values[i])
            if attr == 'codigo':
                entry.config(state='disabled')


class CategoriaFrame(GenericCrudFrame):
    def __init__(self, parent):
        super().__init__(parent, Categoria, "categorias", [("Código", "codigo"), ("Nombre", "nombre")])

class ProductoFrame(GenericCrudFrame):
    def __init__(self, parent):
        super().__init__(parent, Producto, "productos", [
            ("Código", "codigo"), 
            ("Nombre", "nombre"), 
            ("ID Categoría", "categoria_id"), 
            ("ID Proveedor", "proveedor_id"),
            ("Precio Venta", "precio"),
            ("Stock", "cantidad")
        ])
        if 'cantidad' in self.entries:
            self.entries['cantidad'].config(state='disabled')

class ClienteFrame(GenericCrudFrame):
    def __init__(self, parent):
        super().__init__(parent, Cliente, "clientes", [
            ("Código", "codigo"), 
            ("Cédula", "cedula"),
            ("Nombre Completo", "nombre"),
            ("Provincia", "provincia"),
            ("Teléfono", "telefono"),
            ("Correo", "correo")
        ])

class ProveedorFrame(GenericCrudFrame):
    def __init__(self, parent):
         super().__init__(parent, Proveedor, "proveedores", [
            ("Código", "codigo"), 
            ("Cédula", "cedula"),
            ("Nombre Empresa", "nombre"),
            ("Teléfono", "telefono"),
            ("Correo", "correo")
        ])

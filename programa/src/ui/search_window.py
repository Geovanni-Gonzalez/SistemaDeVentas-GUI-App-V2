import tkinter as tk
from tkinter import ttk, messagebox
from src.repository import Repository
from src.models import Factura, DetalleFactura, Producto, OrdenCompra
from src.ui.theme import Theme

class SearchTransactionsWindow(tk.Toplevel):
    def __init__(self, parent, mode="INVOICE"): # mode: INVOICE or ORDER
        super().__init__(parent)
        self.mode = mode
        title = "Buscar Facturas" if mode == "INVOICE" else "Buscar Órdenes de Compra"
        self.title(title)
        self.geometry("700x500")
        Theme.apply_styles(self)
        
        self.repo_main = Repository("facturas" if mode == "INVOICE" else "ordenes")
        self.repo_det = Repository("detalle_facturas" if mode == "INVOICE" else "detalle_ordenes")
        self.repo_prod = Repository("productos")
        
        # Search Bar
        frame_top = ttk.Frame(self)
        frame_top.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_top, text="Número:").pack(side='left')
        self.entry_search = ttk.Entry(frame_top)
        self.entry_search.pack(side='left', padx=5)
        ttk.Button(frame_top, text="Buscar", command=self.perform_search).pack(side='left')
        
        # Results Area
        self.tree = ttk.Treeview(self, columns=("ID", "Fecha", "Entidad", "Total"), show='headings')
        self.tree.heading("ID", text="Número")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Entidad", text="Cliente" if mode == "INVOICE" else "Proveedor")
        self.tree.heading("Total", text="Total")
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Details Area
        self.detail_tree = ttk.Treeview(self, columns=("ProdID", "Cant", "Precio"), show='headings', height=5)
        self.detail_tree.heading("ProdID", text="Producto ID")
        self.detail_tree.heading("Cant", text="Cantidad")
        self.detail_tree.heading("Precio", text="Precio Unit.")
        self.detail_tree.pack(fill='x', padx=10, pady=5)
        
        # Actions
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.btn_anulate = ttk.Button(btn_frame, text="ANULAR", style="Danger.TButton", command=self.anulate_transaction)
        self.btn_anulate.pack(side='right')
        
        self.perform_search() # Load all initially

    def perform_search(self):
        query = self.entry_search.get()
        # Clear
        for item in self.tree.get_children(): self.tree.delete(item)
        
        # Load
        # Determine model class dynamically is tricky with current setup, hardcoding maps
        cls = Factura if self.mode == "INVOICE" else OrdenCompra
        items = self.repo_main.load_all(cls.from_row)
        
        for item in items:
            # Filter
            if query and query != str(item.codigo): continue
            
            entidad_id = item.cliente_id if self.mode == "INVOICE" else item.proveedor_id
            self.tree.insert('', 'end', values=(item.codigo, item.fecha, entidad_id, f"{item.total:.2f}"))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        
        trans_id = int(self.tree.item(sel[0], 'values')[0])
        
        # Load Details
        from src.models import DetalleOrden, DetalleFactura
        cls_det = DetalleFactura if self.mode == "INVOICE" else DetalleOrden
        
        all_dets = self.repo_det.load_all(cls_det.from_row)
        
        # Filter details for this transaction
        # Attribute is 'factura_id' or 'orden_id'
        attr_key = 'factura_id' if self.mode == "INVOICE" else 'orden_id'
        
        relevant = [d for d in all_dets if getattr(d, attr_key) == trans_id]
        
        for item in self.detail_tree.get_children(): self.detail_tree.delete(item)
        
        for d in relevant:
            self.detail_tree.insert('', 'end', values=(d.producto_id, d.cantidad, d.precio_unitario))


    def anulate_transaction(self):
        sel = self.tree.selection()
        if not sel: return
        trans_id = int(self.tree.item(sel[0], 'values')[0])
        
        confirm = messagebox.askyesno("Confirmar Anulación", "Esta acción revertirá el inventario. ¿Continuar?")
        if not confirm: return
        
        # Logic
        # 1. Get Details
        from src.models import DetalleOrden, DetalleFactura
        cls_det = DetalleFactura if self.mode == "INVOICE" else DetalleOrden
        
        all_dets = self.repo_det.load_all(cls_det.from_row)
        attr_key = 'factura_id' if self.mode == "INVOICE" else 'orden_id'
        relevant = [d for d in all_dets if getattr(d, attr_key) == trans_id]
        
        # 2. Update Stock
        stock_repo = Repository("productos")
        prods = stock_repo.load_all(Producto.from_row)
        
        for det in relevant:
            prod = next((p for p in prods if p.codigo == det.producto_id), None)
            if prod:
                if self.mode == "INVOICE":
                    # Anulate Sale = Return stock
                    prod.cantidad += det.cantidad
                else:
                    # Anulate Purchase = Remove stock
                    prod.cantidad -= det.cantidad
                    if prod.cantidad < 0:
                        messagebox.showerror("Error", f"No se puede anular: Stock de producto {prod.codigo} quedaría negativo.")
                        return

        # Commit Stock Changes
        for det in relevant:
            prod = next((p for p in prods if p.codigo == det.producto_id), None)
            if prod: stock_repo.update(prod)
        
        # 3. Delete Transaction
        self.repo_main.delete(trans_id)
        
        # Cleanup details
        # For SQL, we should delete details by ID, but we need the Detail IDs or just execute DELETE FROM child where parent=id
        # My Repo delete() takes an ID (pk).
        # I need to delete the detail rows one by one or create a delete_where method.
        # For now, loop and delete.
        for det in relevant:
            self.repo_det.delete(det.id)
            
        
        messagebox.showinfo("Éxito", "Transacción anulada e inventario actualizado.")
        self.perform_search()
        
        # Refresh details
        for item in self.detail_tree.get_children(): self.detail_tree.delete(item)

import tkinter as tk
from tkinter import ttk, messagebox
from .crud_frames import CategoriaFrame, ProductoFrame, ClienteFrame, ProveedorFrame
from .orders_window import OrdersWindow
from .billing_window import BillingWindow
from src.ui.theme import Theme
from src.repository import Repository
from src.models import Producto

class MainMenu:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        Theme.apply_styles(root)
        
        # Configure MenuBar (Requirement 3.c)
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # Administración
        menu_admin = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Administración", menu=menu_admin)
        menu_admin.add_command(label="Categorías", command=lambda: self.show_module("Categorías", CategoriaFrame))
        menu_admin.add_command(label="Productos", command=lambda: self.show_module("Productos", ProductoFrame))
        menu_admin.add_command(label="Clientes", command=lambda: self.show_module("Clientes", ClienteFrame))
        menu_admin.add_command(label="Proveedores", command=lambda: self.show_module("Proveedores", ProveedorFrame))
        
        # Punto de Venta
        menu_pos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Punto de Venta", menu=menu_pos)
        menu_pos.add_command(label="Facturación", command=self.open_billing)
        menu_pos.add_command(label="Orden de Compra", command=self.open_orders)
        menu_pos.add_separator()
        menu_pos.add_command(label="Búsqueda de Facturas", command=self.open_search_invoices)
        menu_pos.add_command(label="Búsqueda de Órdenes", command=self.open_search_orders)
        
        # Reports
        menu_rep = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=menu_rep)
        menu_rep.add_command(label="Listado de Invoices", command=lambda: self.gen_report('INVOICES'))
        menu_rep.add_command(label="Listado de Órdenes", command=lambda: self.gen_report('ORDERS'))
        
        # Salir
        menubar.add_command(label="Salir", command=root.quit)
        
        # --- Dashboard Area ---
        self.container = ttk.Frame(root)
        self.container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.container.winfo_children():
            widget.destroy()
            
        ttk.Label(self.container, text=f"Bienvenido, {self.user.full_name}", style="H1.TLabel").pack(anchor='w', pady=20)
        # Stats Row
        stats_frame = ttk.Frame(self.container)
        stats_frame.pack(fill='x', pady=20)
        
        # Load Data
        repo_prod = Repository("productos")
        prods = repo_prod.load_all(Producto.from_row)
        
        low_stock = sum(1 for p in prods if p.cantidad < 5)
        total_items = sum(p.cantidad for p in prods)
        
        self.create_card(stats_frame, "Total Productos", f"{len(prods)}", "#3498db")
        self.create_card(stats_frame, "Unidades en Stock", f"{total_items}", "#2ecc71")
        self.create_card(stats_frame, "Stock Bajo", f"{low_stock}", "#e74c3c")

        # --- INNOVATION: Matplotlib Chart ---
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            import matplotlib.pyplot as plt
            
            # Chart Frame
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Prepare Data for Chart (Top Stock)
            top_prods = sorted(prods, key=lambda p: p.cantidad, reverse=True)[:5]
            names = [p.nombre for p in top_prods]
            stocks = [p.cantidad for p in top_prods]

            # Dark Theme for Chart
            from src.ui.theme import Theme
            plt.style.use('dark_background')
            
            fig = Figure(figsize=(5, 3), dpi=100)
            fig.patch.set_facecolor(Theme.BG_MAIN) # Match app bg
            
            ax = fig.add_subplot(111)
            ax.set_facecolor(Theme.BG_MAIN)
            
            bars = ax.bar(names, stocks, color=Theme.PRIMARY)
            
            ax.set_title('Top 5 Productos (Stock)', fontsize=10, color=Theme.TEXT_LIGHT)
            ax.tick_params(axis='x', rotation=15, labelsize=8, colors=Theme.TEXT_MUTED)
            ax.tick_params(axis='y', colors=Theme.TEXT_MUTED)
            ax.spines['bottom'].set_color(Theme.TEXT_MUTED)
            ax.spines['top'].set_color('none') 
            ax.spines['left'].set_color(Theme.TEXT_MUTED)
            ax.spines['right'].set_color('none')
            
            fig.tight_layout()

            chart_frame = tk.Frame(self.container, bg=Theme.BG_MAIN)
            chart_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().configure(bg=Theme.BG_MAIN) # Native widget bg
            canvas.get_tk_widget().pack(side='left', fill='both', expand=True)
            
            # --- AI WIDGET ---
            # Update LabelFrame style manually since ttk style is global but frame needs distinct look
            ai_frame = tk.LabelFrame(chart_frame, text="🤖 Predicción IA", padx=10, pady=10, 
                                   bg=Theme.BG_DARK, fg=Theme.ACCENT, font=("Segoe UI", 10, "bold"), bd=0)
            ai_frame.pack(side='right', fill='both', expand=True, padx=10)
            
            from src.analytics import SalesPredictor
            predictor = SalesPredictor()
            
            risk_prods = []
            for p in prods:
                days = predictor.predict_days_remaining(p.codigo, p.cantidad)
                if days is not None and days < 7:
                    risk_prods.append((p.nombre, days))
            predictor.close()
            
            if risk_prods:
                for name, days in risk_prods:
                    color = "red" if days <= 3 else "orange"
                    msg = "¡Hoy!" if days == 0 else f"en {days} días"
                    tk.Label(ai_frame, text=f"⚠ {name}: Agota {msg}", fg=color, font=("Arial", 10, "bold")).pack(anchor='w')
            else:
                tk.Label(ai_frame, text="✅ Todo en orden. Sin riesgo inmediato.", fg="green").pack()
                
        except ImportError:
            tk.Label(self.container, text="Matplotlib no instalado").pack()
        except Exception as e:
            tk.Label(self.container, text=f"Error en gráfico/IA: {str(e)}", fg="red").pack()
        
        # Actions
        act_frame = ttk.Frame(self.container)
        act_frame.pack(fill='x', pady=20)
        ttk.Label(act_frame, text="Accesos Rápidos", style="H2.TLabel").pack(anchor='w', pady=(0, 10))
        
        ttk.Button(act_frame, text="Nueva Venta", command=self.open_billing).pack(side='left', padx=10)
        ttk.Button(act_frame, text="Reabastecer (Orden)", command=self.open_orders).pack(side='left', padx=10)

    def create_card(self, parent, title, value, color):
        # removed col_idx arg as I am packing now in stats_frame? 
        # Wait, previous code used grid.
        # My replacement code packs stats_frame.
        # But create_stat_card implementation used grid.
        # Let's see how I called it: create_card(stats_frame, ..., color)
        # The original Create Stat Card used grid row=0, col=col_idx.
        # I removed col_idx from call. I should switch to pack side=left or grid.
        # Let's use pack side left with a wrapper frame or just grid since stats_frame is new.
        
        card = tk.Frame(parent, bg=color, padx=20, pady=20)
        card.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(card, text=value, font=("Segoe UI", 32, "bold"), fg="white", bg=color).pack()
        tk.Label(card, text=title, font=("Segoe UI", 12), fg="white", bg=color).pack()

    def show_module(self, title, frame_class):
        for widget in self.container.winfo_children():
            widget.destroy()
            
        header = tk.Frame(self.container, bg=Theme.BG_MAIN)
        header.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header, text=title, style="H1.TLabel").pack(side='left')
        ttk.Button(header, text="Volver al Inicio", command=self.show_dashboard).pack(side='right')
        
        content = frame_class(self.container)
        content.pack(fill='both', expand=True)

    def open_orders(self):
        OrdersWindow(self.root)

    def open_billing(self):
        BillingWindow(self.root)
        
    def open_search_invoices(self):
        from src.ui.search_window import SearchTransactionsWindow
        SearchTransactionsWindow(self.root, mode="INVOICE")
        
    def open_search_orders(self):
        from src.ui.search_window import SearchTransactionsWindow
        SearchTransactionsWindow(self.root, mode="ORDER")

    def gen_report(self, rtype):
        try:
            from src.reports import PDFGenerator
            from src.repository import Repository
            from src.models import Factura, OrdenCompra
            
            # Generate Report (Standardized call remains same as reports.py inherits FPDF)
            # But wait, PDFGenerator INHERITS FPDF now. We must instantiate it.
            # The method signature for generate_list_report is `self.generate_list_report(...)`
            # Wait, PyFPDF usage: `pdf = PDFGen()`. 
            # My modified code in `src/report.py`: `class PDFGenerator(FPDF):`
            # and methods use `self.add_page()`.
            # So usage `gen = PDFGenerator()` is correct.
            
            gen = PDFGenerator()
            if rtype == 'INVOICES':
                repo = Repository("facturas.txt")
                items = repo.load_all(Factura.from_string)
                data = [[i.codigo, i.fecha, i.cliente_id, f"{i.total:.2f}"] for i in items]
                path = gen.generate_list_report("Reporte de Facturas", ["ID", "Fecha", "Cliente", "Total"], data, "Reporte_Facturas")
            else:
                repo = Repository("ordenes.txt")
                items = repo.load_all(OrdenCompra.from_string)
                data = [[i.codigo, i.fecha, i.proveedor_id, f"{i.total:.2f}"] for i in items]
                path = gen.generate_list_report("Reporte de Órdenes", ["ID", "Fecha", "Prov", "Total"], data, "Reporte_Ordenes")
            
            messagebox.showinfo("Éxito", f"Reporte generado en: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo generando reporte: {e}")

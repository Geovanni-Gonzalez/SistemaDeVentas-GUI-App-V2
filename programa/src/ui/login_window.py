import tkinter as tk
from tkinter import ttk, messagebox
from src.auth import AuthController
from src.ui.theme import Theme

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Login - Sistema de Ventas")
        self.root.geometry("400x450")
        
        # Apply Theme
        Theme.apply_styles(root)
        root.configure(bg=Theme.BG_DARK) # Dark background for Login
        
        self.auth = AuthController()

        # Login Frame (Card)
        card = tk.Frame(root, bg=Theme.BG_MAIN, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(card, text="Iniciar Sesión", style="H1.TLabel").pack(pady=(0, 20))

        ttk.Label(card, text="Usuario:").pack(fill='x')
        self.entry_user = ttk.Entry(card)
        self.entry_user.pack(fill='x', pady=(0, 15))

        ttk.Label(card, text="Contraseña:").pack(fill='x')
        self.entry_pass = ttk.Entry(card, show="*")
        self.entry_pass.pack(fill='x', pady=(0, 20))

        ttk.Button(card, text="INGRESAR", command=self.do_login, width=20).pack()
        
        tk.Label(card, text="Sistema de Ventas v2.0", bg=Theme.BG_MAIN, fg=Theme.TEXT_MUTED, font=("Arial", 8)).pack(pady=(30,0))

    def do_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        user = self.auth.login(u, p)
        if user:
            self.on_success(user)
        else:
            messagebox.showerror("Error", "Credenciales Inválidas")

import tkinter as tk
from src.ui.login_window import LoginWindow
from src.ui.main_menu import MainMenu
from src.database import DatabaseManager

def main():
    DatabaseManager.initialize_db()
    root = tk.Tk()
    
    def start_app(user):
        # Placeholder for Main Menu transition
        # print(f"Login Success: {user.full_name}")
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("800x600")
        root.title(f"Sistema de Ventas - Usuario: {user.full_name}")
        # tk.Label(root, text="Bienvenido al Sistema").pack()
        MainMenu(root, user)

    LoginWindow(root, start_app)
    root.mainloop()

if __name__ == "__main__":
    main()

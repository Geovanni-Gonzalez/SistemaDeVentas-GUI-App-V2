import tkinter as tk
from tkinter import ttk

class Theme:
    # Catppuccin / Cyber Palette
    BG_DARK = "#1e1e2e"     # Base
    BG_MAIN = "#181825"     # Mantle
    
    PRIMARY = "#89b4fa"     # Blue
    SECONDARY = "#f5c2e7"   # Pink
    ACCENT = "#cba6f7"      # Mauve
    
    TEXT_LIGHT = "#cdd6f4"  # Text
    TEXT_DARK = "#1e1e2e"   # Crust
    TEXT_MUTED = "#a6adc8"  # Subtext
    
    SUCCESS = "#a6e3a1"     # Green
    DANGER = "#f38ba8"      # Red
    WARNING = "#fab387"     # Peach

    FONT_H1 = ("Segoe UI", 24, "bold")
    FONT_H2 = ("Segoe UI", 16, "bold")
    FONT_BODY = ("Segoe UI", 11)
    FONT_BOLD = ("Segoe UI", 11, "bold")

    @staticmethod
    def apply_styles(root):
        style = ttk.Style(root)
        style.theme_use('clam') 

        # General Frame
        style.configure("TFrame", background=Theme.BG_MAIN)
        
        # Labels
        style.configure("TLabel", background=Theme.BG_MAIN, foreground=Theme.TEXT_LIGHT, font=Theme.FONT_BODY)
        style.configure("H1.TLabel", font=Theme.FONT_H1, foreground=Theme.PRIMARY)
        style.configure("H2.TLabel", font=Theme.FONT_H2, foreground=Theme.ACCENT)
        style.configure("Muted.TLabel", foreground=Theme.TEXT_MUTED, font=("Segoe UI", 9))
        
        # Buttons (TButton)
        style.configure("TButton", 
                        font=Theme.FONT_BOLD, 
                        background=Theme.PRIMARY, 
                        foreground=Theme.BG_DARK, 
                        borderwidth=0, 
                        focuscolor=Theme.SECONDARY,
                        padding=10)
        style.map("TButton", 
                  background=[('active', Theme.SECONDARY)],
                  foreground=[('active', Theme.BG_DARK)])
                  
        # Danger Button
        style.configure("Danger.TButton", background=Theme.DANGER, foreground=Theme.BG_DARK)
        style.map("Danger.TButton", background=[('active', "#d20f39")])
        
        # Treeview
        style.configure("Treeview", 
                        background=Theme.BG_DARK,
                        foreground=Theme.TEXT_LIGHT,
                        rowheight=30,
                        fieldbackground=Theme.BG_DARK,
                        font=Theme.FONT_BODY,
                        borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        font=Theme.FONT_BOLD, 
                        background=Theme.BG_MAIN, 
                        foreground=Theme.PRIMARY,
                        relief="flat")
                        
        style.map("Treeview", background=[('selected', Theme.ACCENT)], foreground=[('selected', Theme.BG_DARK)])
        
        # Notebook
        style.configure("TNotebook", background=Theme.BG_MAIN, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        font=Theme.FONT_BOLD, 
                        padding=[15, 8], 
                        background=Theme.BG_DARK, 
                        foreground=Theme.TEXT_MUTED,
                        borderwidth=0)
        style.map("TNotebook.Tab", 
                  background=[('selected', Theme.PRIMARY)], 
                  foreground=[('selected', Theme.BG_DARK)])

        # Entry
        style.configure("TEntry", 
                        fieldbackground=Theme.BG_DARK, 
                        foreground=Theme.TEXT_LIGHT,
                        insertcolor="white",
                        padding=5,
                        borderwidth=1,
                        relief="solid")

        # Labelframes
        style.configure("TLabelframe", background=Theme.BG_MAIN, foreground=Theme.PRIMARY, bordercolor=Theme.ACCENT)
        style.configure("TLabelframe.Label", background=Theme.BG_MAIN, foreground=Theme.PRIMARY, font=Theme.FONT_BOLD)

        root.configure(bg=Theme.BG_MAIN)

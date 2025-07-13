import customtkinter as ctk
import win32gui
import win32con
import ctypes
import threading
import tkinter.messagebox as messagebox
from rpc import RPC
import time


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.rpc = RPC()

        self.title("Custom Discord RPC by SCPROGRAMS / SCPTOM")
        self.geometry("800x600")
        self.minsize(700, 500)
        self.maxsize(700, 500)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.button_home = ctk.CTkButton(self.sidebar, text="Home", command=lambda: self.show_frame("home"))
        self.button_home.grid(row=1, column=0, padx=20, pady=10)

        self.button_settings = ctk.CTkButton(self.sidebar, text="Settings", command=lambda: self.show_frame("settings"))
        self.button_settings.grid(row=2, column=0, padx=20, pady=10)

        self.button_about = ctk.CTkButton(self.sidebar, text="About", command=lambda: self.show_frame("about"))
        self.button_about.grid(row=3, column=0, padx=20, pady=10)

        self.button_exit = ctk.CTkButton(self.sidebar, text="Exit", fg_color = "#ff0000", command=self.quit)
        self.button_exit.grid(row=6, column=0, padx=20, pady=20, sticky="s")


        self.pages = {
            "home": self.create_home_page(),
            "settings": self.create_settings_page(),
            "about": self.create_about_page(),
        }

        self.show_frame("home")

    def hide_all_pages(self):
        for page in self.pages.values():
            page.grid_forget()

    def show_frame(self, name):
        self.hide_all_pages()
        self.pages[name].grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def create_home_page(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        row_num = 0
        label = ctk.CTkLabel(frame, text="🏠 Home Page", font=ctk.CTkFont(size=18))
        label.grid(row=row_num, column=0, padx=20, pady=20, columnspan=3)
        row_num += 1

        if self.rpc.getConnected():

            self.bigTextLabel = ctk.CTkLabel(frame, text="Big image hover text")
            self.bigTextLabel.grid(row=row_num, column=0, pady=(0, 2))

            self.smallTextLabel = ctk.CTkLabel(frame, text="Small image hover text")
            self.smallTextLabel.grid(row=row_num, column=1, pady=(0, 2))

            self.deailsTextLabel = ctk.CTkLabel(frame, text="Details text")
            self.deailsTextLabel.grid(row=row_num, column=2, pady=(0, 2))
            row_num += 1

            
            self.bigTextBox = ctk.CTkEntry(frame, placeholder_text=self.rpc.getLargeText())
            self.bigTextBox.grid(row=row_num, column=0, pady=(0, 10), padx=10, sticky="ew")

            self.smallTextBox = ctk.CTkEntry(frame, placeholder_text=self.rpc.getSmallText())
            self.smallTextBox.grid(row=row_num, column=1, pady=(0, 10), padx=10, sticky="ew")

            self.detailsBox = ctk.CTkEntry(frame, placeholder_text=self.rpc.getDetails())
            self.detailsBox.grid(row=row_num, column=2, pady=(0, 10), padx=10, sticky="ew")
            row_num += 1


            self.stateTextLabel = ctk.CTkLabel(frame, text="State text")
            self.stateTextLabel.grid(row=row_num, column=0, pady=(0, 2))

            self.extraLabel1 = ctk.CTkLabel(frame, text="Large Image")
            self.extraLabel1.grid(row=row_num, column=1, pady=(0, 2))

            self.extraLabel2 = ctk.CTkLabel(frame, text="Small Image")
            self.extraLabel2.grid(row=row_num, column=2, pady=(0, 2))
            row_num += 1

    
            self.stateBox = ctk.CTkEntry(frame, placeholder_text=self.rpc.getState())
            self.stateBox.grid(row=row_num, column=0, pady=(0, 10), padx=10, sticky="ew")

            self.largeImageBox = ctk.CTkEntry(frame, placeholder_text="Large Image Name")
            self.largeImageBox.grid(row=row_num, column=1, pady=(0, 10), padx=10, sticky="ew")

            self.smallImageBox = ctk.CTkEntry(frame, placeholder_text="Small Image Name")
            self.smallImageBox.grid(row=row_num, column=2, pady=(0, 10), padx=10, sticky="ew")
            row_num += 1


            self.updateButton = ctk.CTkButton(
                frame,
                text="Update RPC",
                command=self.update_rpc_from_fields
            )
            self.updateButton.grid(row=row_num, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
            row_num += 1

            self.disconnectButton = ctk.CTkButton(
                frame,
                text="Disconnect RPC",
                command=self.disconnect
            )
            self.disconnectButton.grid(row=row_num, column=0, columnspan=3, pady=(0, 20), padx=10, sticky="ew")
            row_num += 1

        else:
            startButton = ctk.CTkButton(
                frame,
                text="Start RPC",
                command=self.start_rpc_thread,
                width=150,
                height=40,
                font=ctk.CTkFont(size=16)
            )
            startButton.grid(row=row_num, column=1, padx=20, pady=10)
            row_num += 5

        return frame
    
    def update_rpc_from_fields(self):
        self.rpc.setLargeText(self.bigTextBox.get())
        self.rpc.setState(self.stateBox.get())
        self.rpc.setDetails(self.detailsBox.get())
        self.rpc.setSmallText(self.smallTextBox.get())
        self.rpc.setLargeImage(self.largeImageBox.get())
        self.rpc.setSmallImage(self.smallImageBox.get())

        if self.rpc.updateRPC():
            print("RPC Updated!")
        else:
            print("Failed to update RPC.")

    def start_rpc_thread(self):
        print("DEBUG: Starting RPC thread...")
        def target():
            print("DEBUG: RPC thread target function started.")
            connected = self.rpc.initRPC()
            self.rpc.connected = connected
            print(f"DEBUG: RPC connection attempt finished. Connected: {self.rpc.getConnected()}")
            self.after(0, self.refresh_home_page)
        threading.Thread(target=target, daemon=True).start()

    def disconnect(self):
        print("DEBUG: Disconnect button clicked.")
        if self.rpc.closeRPC():
            print("DEBUG: RPC successfully disconnected.")
        else:
            print("DEBUG: RPC disconnection failed or was already disconnected.")
        self.refresh_home_page()

    def refresh_home_page(self):
        print("DEBUG: refresh_home_page called.")

        if "home" in self.pages and self.pages["home"].winfo_exists():
            self.pages["home"].destroy()
            print("DEBUG: Old home page destroyed.")
        else:
            print("DEBUG: Old home page not found or already destroyed.")
        

        self.pages["home"] = self.create_home_page()
        self.show_frame("home")
        print("DEBUG: New home page created and shown.")

    def create_settings_page(self):
        frame = ctk.CTkFrame(self, corner_radius=15)

        row_num = 0

        label = ctk.CTkLabel(frame, text="⚙️ Settings Page", font=ctk.CTkFont(size=18))
        label.grid(row=row_num, column=0, padx=20, pady=(20, 10))
        row_num += 1

        clientIDBox = ctk.CTkEntry(frame, placeholder_text=self.rpc.getClientID())
        clientIDBox.grid(row=row_num, column=0, pady=10)
        row_num += 1

        clientIDButton = ctk.CTkButton(frame, text="Set Client ID", command=lambda: self.rpc.setClientID(clientIDBox.get()))
        clientIDButton.grid(row=row_num, column=0, pady=10)
        row_num += 1

        return frame

    def create_about_page(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        label = ctk.CTkLabel(frame, text="ℹ️ About Page", font=ctk.CTkFont(size=18))
        label.pack(padx=20, pady=20)
        desc = ctk.CTkLabel(frame, text="Made by SCPROGRAMS / SCPTOM\nTwitter: @Pastingsince06", justify="left")
        desc.pack(pady=10)
        return frame


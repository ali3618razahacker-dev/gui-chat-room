import socket
import threading
import customtkinter as ctk
from tkinter import simpledialog, messagebox

HOST = "localhost"
PORT = 2221
destroy = False

# ---------------- SOCKET ----------------
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
except:
    messagebox.showerror("Error", "Cannot connect to server")
    destroy = True

# ---------------- THEME (FORCED DARK) ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- THEME COLORS (DARK ONLY) ----------------
chat_bg = "#333333"
text_color = "white"
entry_bg = "#555555"

# ---------------- USERNAME ----------------
username = simpledialog.askstring("Username", "Please enter your username:")
if not username:
    destroy = True

if destroy:
    exit()

# ---------------- GUI ----------------
root = ctk.CTk()
root.title(username)
root.geometry("520x533")
# root.resizable(False, False)

# Chat Area
chat_area = ctk.CTkTextbox(
    root,
    text_color=text_color,
    fg_color=chat_bg,
    width=500,
    height=450,
    font=("Arial", 16)
)
chat_area.pack(padx=10, pady=10)
chat_area.configure(state="disabled")

# settings button
set_btn = ctk.CTkButton(root, text="⚙️", corner_radius=100, width=10, height=40, font=('Arial', 20))
set_btn.pack(side=ctk.LEFT, padx=5)
# Message Entry
msg_entry = ctk.CTkEntry(
    root,
    placeholder_text="Enter the message",
    width=350,
    corner_radius=20,
    height=40,
    fg_color=entry_bg,
    text_color=text_color
)
msg_entry.pack(side=ctk.LEFT, padx=0, pady=10)

# Send Button
send_button = ctk.CTkButton(
    root,
    text="Send",
    corner_radius=20,
    height=40
)
send_button.pack(side=ctk.RIGHT, padx=5, pady=10)

# ---------------- FUNCTIONS ----------------
def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "USER":
                client.send(username.encode("ascii"))
            else:
                chat_area.configure(state="normal")
                chat_area.insert("end", message + "\n")
                chat_area.configure(state="disabled")
                chat_area.yview("end")
        except:
            break

def send(event=None):
    message = msg_entry.get()
    if message.strip() == "":
        return
    msg_entry.delete(0, ctk.END)
    try:
        client.send(f"{username}: {message}".encode("ascii"))
    except:
        messagebox.showerror("Error", "Failed to send message")

def apply_theme(theme):
    ctk.set_appearance_mode(theme)
    if theme == "dark":
        chat_area.configure(fg_color="#333333", text_color="white")
        msg_entry.configure(fg_color="#555555", text_color="white")
    else:
        chat_area.configure(fg_color="#B3A2A2", text_color="black")
        msg_entry.configure(fg_color="#a58c8c", text_color="black")

def open_setting(argument=None):
    settings_win = ctk.CTkToplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("220x220")
    settings_win.resizable(False, False)
    settings_win.transient(root)

    ctk.CTkLabel(settings_win, text="Theme settings", font=("Arial", 16)).pack(pady=10)

    theme_var = ctk.StringVar(value=ctk.get_appearance_mode().lower())

    def on_theme_change():
        apply_theme(theme_var.get())

    ctk.CTkRadioButton(settings_win, text="Light", variable=theme_var, value="light").pack(pady=5)
    ctk.CTkRadioButton(settings_win, text="Dark", variable=theme_var, value="dark").pack(pady=5)
    ctk.CTkButton(settings_win, text="Apply", command=on_theme_change).pack(pady=15)




msg_entry.bind("<Return>", send)
send_button.configure(command=send)

set_btn.configure(command=open_setting)

# ---------------- THREAD ----------------
thread = threading.Thread(target=receive, daemon=True)
thread.start()

root.mainloop()

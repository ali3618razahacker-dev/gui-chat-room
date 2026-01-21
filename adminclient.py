import socket
import threading
import customtkinter as ctk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = "localhost"
PORT = 2221

try:   
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
except Exception as e:
    messagebox.showerror("Error", f"connection refused code: {e}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

username = simpledialog.askstring("Username", "Please enter your username:")

root = ctk.CTk()
root.title(username)
root.geometry("800x560")
# root.resizable(False, False)

# left frame with chat areaa and the entry and teh send

left_frame = ctk.CTkFrame(root, width=650, height=500, fg_color="#3d6978", corner_radius=20)
left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

# right frame with kil and private command

right_frame = ctk.CTkFrame(root, width=250, fg_color="#3d6978", corner_radius=20)
right_frame.pack(side=ctk.RIGHT, padx=10, pady=10, fill="y")


chat_area = ctk.CTkTextbox(left_frame, width=600, height=450, fg_color="#5C5555", border_color="#7d9992", corner_radius=20, font=("Arial", 16))
chat_area.configure(state="disabled")
chat_area.pack(padx=10, pady=10)

msg_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your message:", width=500, height=50, corner_radius=20)
msg_entry.pack(side=ctk.LEFT, padx=10, pady=10, anchor="w")

send_btn = ctk.CTkButton(left_frame, text="Send", width=65, height=45, corner_radius=20)
send_btn.pack(side=ctk.LEFT)

kick_btn = ctk.CTkButton(right_frame, text="KICK USER", width=80, height=45, fg_color="red", corner_radius=20)
kick_btn.pack(padx=10, pady=10)

prv_btn = ctk.CTkButton(right_frame, text="Private\nmessage", width=100, height=45, fg_color="red", corner_radius=20)
prv_btn.pack(padx=10, pady=10)

clr_btn = ctk.CTkButton(right_frame, text="clear", fg_color="red", width=100, height=45, corner_radius=20)
clr_btn.pack(padx=5, pady=10)

us_ls_btn = ctk.CTkButton(right_frame, text="see users", fg_color="red", width=100, height=45, corner_radius=20)
us_ls_btn.pack(padx=5, pady=10)

# functions
def recieve():
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            decoded = message.decode()

            if decoded == "USER":
                client.send(username.encode('ascii'))
            else:
                chat_area.configure(state="normal")
                chat_area.insert(ctk.END, decoded + "\n")
                chat_area.configure(state="disabled")
                chat_area.see("end")

        except:
            break

def send(argument=None):
    print("send")
    message = msg_entry.get()
    client.send(f"{username}: {message}".encode('ascii'))
    msg_entry.delete(0, "end")

def kick():
    print("kick user")
    user = simpledialog.askstring("Username", "enter username of the person you want to kick:")
    client.send(f"KICK {user}".encode('ascii'))

def prv_msg():
    print("prv_msg")
    user = simpledialog.askstring("user", "enter username of the person: ")
    message = simpledialog.askstring("message", "enter message:")
    client.send(f"PRV {user} {message}".encode('ascii'))

def clear():
    chat_area.configure(state="normal")  # make it editable
    chat_area.delete("1.0", "end")       # delete all text
    chat_area.configure(state="disabled")  # disable editing again

def see_users():
    user_win = ctk.CTk()
    user_win.geometry("250x600")
    user_win.title("Users")

    user_area = ctk.CTkTextbox(user_win, width=240, height=580, state="disabled")

    def update_users():
        client.send("USER_LIST".encode("ascii"))

        list_str = client.recv(1024).decode("ascii")
        users = list_str.split(",")

        user_area.configure(state="normal")
        user_area.delete("1.0", "end")

        for user in users:
            user_area.insert("end", user + "\n")

        user_area.configure(state="disabled")

    update_btn = ctk.CTkButton(
        user_win,
        text="Reload",
        width=240,
        height=45,
        corner_radius=20,
        command=update_users
    )

    update_btn.pack(padx=10, pady=10)
    user_area.pack(padx=10, pady=5)

    user_win.mainloop()


send_btn.configure(command=send)
kick_btn.configure(command=kick)
prv_btn.configure(command=prv_msg)
clr_btn.configure(command=clear)
us_ls_btn.configure(command=see_users)

msg_entry.bind("<Return>", send)

thread = threading.Thread(target=recieve, daemon=True)
thread.start()
root.mainloop()
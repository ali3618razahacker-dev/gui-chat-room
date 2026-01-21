import socket
import threading

HOST = "localhost"
PORT = 2221

clients = []
usernames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


def handle(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            decoded_msg = message.decode('ascii')

            if decoded_msg.startswith("KICK"):
                user = decoded_msg[5:]

                if user in usernames:
                    index = usernames.index(user)
                    cl = clients[index]

                    usernames.remove(user)
                    clients.remove(cl)

                    cl.close()
                    print(f"{user} was kicked")

                continue
            elif decoded_msg.startswith("PRV"):
                parts = decoded_msg.split(" ", 2)
                user = parts[1]
                message = parts[2]
                index = usernames.index(user)
                cl = clients[index]
                cl.send(message.encode("ascii"))

            elif decoded_msg.startswith("USER_LIST"):
                users_str = ",".join(usernames)
                client.send(users_str.encode("ascii"))
            else:
                broadcast(message)

        except:
            break

    # Cleanup on disconnect
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)

        client.close()
        print(f"disconnected {username}")


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("USER".encode('ascii'))
        username = client.recv(1024).decode('ascii')

        clients.append(client)
        usernames.append(username)

        print(f"Username: {username}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server listening.......")
receive()

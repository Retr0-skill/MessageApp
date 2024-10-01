import socket
import threading


def receive_messages(client_socket):
    """Riceve i messaggi dal server e li visualizza correttamente"""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\r{message}\nTu: ", end='', flush=True)
        except:
            print("Connessione chiusa dal server.")
            client_socket.close()
            break

def send_messages(client_socket):
    """Permette di inviare messaggi in modo continuo"""
    while True:
        message = input("Tu: ")
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode())

# Impostazioni del client


server_ip = '127.0.0.1'  # Modifica con l'IP del server
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Riceve il messaggio di richiesta del nome dal server
server_message = client_socket.recv(1024).decode()
print(server_message, end='')

# Invia il nome al server
name = input()
client_socket.send(name.encode())

# Thread per ricevere i messaggi dal server
threading.Thread(target=receive_messages, args=(client_socket,)).start()

# Thread per inviare i messaggi al server
send_messages(client_socket)

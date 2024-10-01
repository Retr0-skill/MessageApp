import socket
import threading
import os

clients = {}  #Dizionario per memorizzare i client con i loro nomi
log_file = 'chat_log.txt'

def save_message(message):
    """Salva i messaggi nel file di log"""
    with open(log_file, 'a') as f:
        f.write(message + '\n')

def load_chat_history():
    """Carica i messaggi dal file di log e li restituisce"""
    if not os.path.exists(log_file):
        return []
    
    with open(log_file, 'r') as f:
        return f.readlines()

def broadcast(message, sender_socket=None):
    """Invia un messaggio a tutti i client connessi tranne il mittente"""
    save_message(message)  # Salva ogni messaggio nel file di log
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, client_address):
    """Gestisce la comunicazione con un singolo client"""
    client_socket.send("Inserisci il tuo nome: ".encode())
    name = client_socket.recv(1024).decode().strip()
    clients[client_socket] = name

    # Invia la cronologia delle chat al client connesso
    chat_history = load_chat_history()
    if chat_history:
        client_socket.send("** Cronologia chat **\n".encode())
        for line in chat_history:
            client_socket.send(line.encode())

    broadcast(f"{name} si è unito alla discussione.", client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(f"{name}: {message}", client_socket)
            else:
                break
        except:
            break

    # Rimuovi il client dalla lista quando si disconnette
    client_socket.close()
    del clients[client_socket]
    broadcast(f"{name} ha abbandonato la ciurma...")

def start_server():
    """Avvia il server per ascoltare connessioni multiple"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '0.0.0.0'
    server_port = 12345
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server avviato su {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione accettata da {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def server_send():
    """Permette al server di inviare messaggi agli host"""
    while True:
        message = input()
        broadcast(f"Server: {message}")

# Avvia i thread per gestire i client e per inviare messaggi dal server
threading.Thread(target=start_server).start()
threading.Thread(target=server_send).start()

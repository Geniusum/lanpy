import pickle
import socket
import threading

def void(*args, **kwargs): return None

class Sender():
    def __init__(self, subnetwork: int, host: int, port_add: int = 0) -> None:
        self.ip_address = f"192.168.{subnetwork}.{host}"
        self.port = 13900 + port_add
        # Initialisation du socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send_object(self, obj: any) -> None:
        try:
            # Connexion au destinataire
            self.sock.connect((self.ip_address, self.port))
            # Sérialisation et envoi de l'objet
            data = pickle.dumps(obj)
            self.sock.sendall(data)
        except Exception as e:
            print(f"Erreur lors de l'envoi : {e}")
        finally:
            self.sock.close()


class Listener():
    def __init__(self, receiver_function, subnetwork: int, host: int, port_add: int = 0) -> None:
        self.ip_address = f"192.168.{subnetwork}.{host}"
        self.port = 13900 + port_add
        self.receiver_function = receiver_function
        self.running = False
        # Initialisation du socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(5)  # Peut gérer jusqu'à 5 connexions simultanées

    def _listen(self):
        self.running = True
        while True:
            try:
                # Accepte une connexion entrante
                conn, addr = self.sock.accept()
                print(f"Connexion reçue de {addr}")
                # Réception des données
                data = conn.recv(4096)  # Taille max de buffer
                if data:
                    # Désérialisation de l'objet et appel de la fonction utilisateur
                    obj = pickle.loads(data)
                    self.receiver_function(obj)
                conn.close()
            except Exception as e:
                self.running = False
                print(f"Erreur lors de la réception : {e}")
                break

    def start_listening(self):
        # Démarre un thread pour l'écoute en boucle
        listener_thread = threading.Thread(target=self._listen, daemon=True)
        listener_thread.start()
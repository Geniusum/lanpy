import lanpy

def receive(obj):
    print(obj)

listener = lanpy.Listener(receive, 0, 23)
listener.start_listening()
print("Listening...")

while listener.running:
    pass
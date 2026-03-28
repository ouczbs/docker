import socket
anki_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
anki_connect.connect(("127.0.0.1", 8765))
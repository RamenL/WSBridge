import thread
import socket
import sys
import time
#https://github.com/vinodpandey/python-port-forward
#https://gist.github.com/Motoma/1215469


def forward(source, destination):
    string = ' '
    while string:
        string = source.recv(1024)
        if string:
            destination.sendall(string)
        else:
            print("attempt to close")
            try: source.close()
            except: pass
            try: destination.close()
            except: pass
            thread.exit()


running = False

try:
    # host agent
    print("Waiting for Host Agent to connect to 8081")
    listener = socket.socket()
    listener.bind(('0.0.0.0', 8081))
    listener.listen(1)
    bridge_client = listener.accept()[0]
    listener.close()
    print("Bridge Client Connected.")

    # guacd
    print("Waiting for Guacd to connect to 8080")
    listener = socket.socket()
    listener.bind(('127.0.0.1', 8080))
    listener.listen(1)
    client = listener.accept()[0]
    listener.close()
    print("Client Connected")

    running = True
except: pass



while running:
    try:
        thread.start_new_thread(forward, (bridge_client, client))
        thread.start_new_thread(forward, (client, bridge_client))
    except:
        pass

try: client.close()
except: pass

try: bridge_client.close()
except: pass

print("Closing.")
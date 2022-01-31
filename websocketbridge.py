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
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)

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
        """
        rlist = select.select([bridge_client, client], [], [])[0]

        if bridge_client in rlist:
            buf = bridge_client.recv(4096)
            if len(buf) == 0:
                print("Bridge Client Disconnected.")
                running = False

            client.send(buf)

        if client in rlist:
            buf = client.recv(4096)
            if len(buf) == 0:
                print("Client Disconnected.")
                running = False

            bridge_client.send(buf)
        """

    except:
        pass

try: client.close()
except: pass

try: bridge_client.close()
except: pass

print("Closing.")
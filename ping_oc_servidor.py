# ping_oc_servidor.py
import socket
import sys
import os
import signal

MAX_DATA_LEN = 64

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def error():
    sock.close()
    sys.exit(-1)

def signal_handler(signal, frame):
    sock.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print ("ERROR: numero de argumentos incorrecto.")
        print ("Uso: python ping_oc_servidor.py [PUERTO]")
        error()

    signal.signal(signal.SIGINT, signal_handler)
    
    port = int(sys.argv[1])
    sock.bind(('', port))
    sock.listen(5)

    print ("Socket creado y asignado.")
    print ("### Log de eventos servidor ###")
    
    global j
    j = 0

    while True:
        conn, addr = sock.accept()
        address = (addr[0],addr[1])
        print ("Cliente conectado (IP[%s], PORT[%s])" %address)

        childServer = os.fork()
        if childServer == 0:
            while True:
                message = "icmp_seq=%s" %j
                try:
                    data = conn.recv(MAX_DATA_LEN).decode()
                except:
                    print ("No se ha podido enviar la respuesta al servidor.")
                    error()

                if not data: break
                datos = (data,addr[0])
                print (" %s from %s" %datos)

                try:
                    conn.send(message.encode())
                    j = j + 1
                except:
                    print ("ERROR: No se pudo enviar el mensaje.")
                    error()

            conn.close()
            sys.exit(0)
        else:
            conn.close()

    sock.close()

if __name__ == "__main__":
    main()

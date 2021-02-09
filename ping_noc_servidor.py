# ping_noc_servidor.py
import socket
import sys
import os
import signal

MAXDATA = 64

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def error():
    sock.close()
    sys.exit(-1)

def signal_handler(signal, frame):
    sock.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print ("ERROR: numero de argumentos incorrecto.")
        print ("Uso: python ping_noc_servidor.py [PUERTO]\n")
        error()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        sock.bind(('', int(sys.argv[1])))
    except:
        print ("ERROR: No se pudo enlazar el socket.")
        error()

    print ("Socket creado y asignado.")
    print ("### Log de eventos del servidor ###")

    global j
    j = 0

    while True:
        message = "icmp_seq=%s" %j
        try:
            data, client = sock.recvfrom(MAXDATA)
        except:
            print ("ERROR: No se pudo recibir el mensaje del cliente.")
            error()
        datos = (data, client)
        print (" %s from %s" %datos)

        try:
            sock.sendto(message.encode(), client)
            j = j + 1
        except:
            print ("ERROR: No se pudo enviar la respuesta al cliente.")
            error()

    sock.close()

if __name__ == "__main__":
    main()

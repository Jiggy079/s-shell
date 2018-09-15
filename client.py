import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(address, port):
    s.connect((address,port))
    print("\n Connected successfully!")
    cwd = s.recv(2048).decode('utf-8')
    prompt = cwd+"> "
    while 1:
        try:
            command = input(prompt).strip()
            s.sendall(command.encode())
            response = s.recv(4096).decode('utf-8')
            if "CWD=" in response:
                cwd = response.split(" ")
                print("\n"+cwd[1]+"\n")


            elif "LS= " in response:
                dirList = []
                for each in response.split("|"):
                    dirList.append(each)
                dirList.pop(0)
                print("\n")
                for each in dirList:
                    print(each)
                print("\n")

            elif "C:\\" in response:
                print("\n")
                prompt = response+"> "
            
            elif "OUTPUT= |" in response:
                outputList = []
                for each in response.split("|"):
                    outputList.append(each)
                outputList.pop(0)
                print("\n")
                for each in outputList:
                    print(each)
                print("\n")


            else:
                print("\n"+response+"\n")
        
        except:
            print("Invalid command")

def main():
    print("-"*50)
    print(" "*13+"Remote Shell Client v0.0.1"+" "*15)
    print(" "*18+"By Jamie Vickers"+" "*15)
    print("-"*50)

    while 1:
        try:
            command = input("> ").strip()
            commandList = command.split(" ")
            helpList = ["?","help","h"]
            
            if commandList[0] in helpList:
                print("\nSyntax:")
                print("connect [address] [port]")
                print("h / ? / help : display this help output\n")

            elif commandList[0] == "connect":
                address = commandList[1]
                port = int(commandList[2])
                print("Connecting to {} on port {}...".format(address,port))
                connect(address,port)

        except Exception as e:
            print("An error occured: "+str(e))


if __name__=="__main__":
    main()

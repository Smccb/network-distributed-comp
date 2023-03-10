import socket
import threading

from time import gmtime, strftime
import time


HOST = '0.0.0.0'        
PORT = 50007              
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


  
    
# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""   

# custom say hello command
def sayHello():
    print ("----> The hello function was called")
    

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, con):
    print("parsing...")
    print(str(data))
    
    #hello command
    # Checking for commands 
    if "<hello>" in data:
        print("command in data..")
        con.send(str("we got the hello").encode())

    #getFile command, reads in and sends the bytes
    elif "<getfile" in data:
        print('got britney request...again....')

        #cleaning
        parts = data.split('-') #split on the dash

        #only gradb last filename
        filename = parts[1] #turn into an array
        filename = filename[:-3] #remove last 3 chars

        #read bytes for britney file
        with open(filename , 'rb') as f:
            fileContent = f.read()
            print(fileContent)

            #send britney bytes back
            con.send(fileContent)
            f.close()


    #splits command, breaks file up into 2 seperate files
    elif "<split" in data:

        #cleaning
        parts = data.split('-') #split on the dash

        #only gradb last filename
        filename = parts[1] #turn into an array
        filename = filename[:-3] #remove last 3 chars

        with open(filename, mode="rb") as file:
            contents = file.read()

            chunkSize = 1000*500
            f = open('1.mp3', 'wb+')
            f.write(contents[0:chunkSize])
            f.close()
            f = open('2.mp3', 'wb+')
            f.write(contents[chunkSize:chunkSize*2])
            f.close()


    #delete command, removes both mp3 files
    elif "<delete" in data:
        print("delete" + filename)

        #cleaning
        parts = data.split('-') #split on the dash

        #only gradb last filename
        filename = parts[1] #turn into an array
        filename = filename[:-3] #remove last 3 chars

        import os
        os.remove(filename)


    #hash command, reads the filename after the hash part and hashes it
    elif "<hash" in data:
        import hashlib

        #cleaning
        parts = data.split('-') #split on the dash

        #only gradb last filename
        filename = parts[1] #turn into an array
        filename = filename[:-3] #remove last 3 chars


        # get the file bytes
        file = open(filename, 'rb')
        content = file.read()
        m = hashlib.sha256()
        # get the hash
        m.update(content)
        res = m.digest()
        print(res)


    #list all items in directory
    elif "<list>" in data:
        import os



        print("list files")
        path = "." #path to home dir
        dir_list: list = os.listdir(path) #create a list of all items in directory

        print("Files and directories in '", path, "' :")

        newList = []

        #copy items with substring .mp3 to new list
        for i, filename in enumerate(dir_list):
        
            if ".mp3" in filename:
                newList.append(filename)

        print(newList)
            

        con.send(str(newList).encode())#send newList to client
        
    
# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.
    
def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)
    
    
    data = conn.recv(1024)
    
    parseInput(str(data), conn)# Calling the parser, passing the connection
    
    print("rec:" + str(data))
    buffer += str(data)
    
    #conn.send(str(buffer))
        
    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))
    
    t.start()
    
    



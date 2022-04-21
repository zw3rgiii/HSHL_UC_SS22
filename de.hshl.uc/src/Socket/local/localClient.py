import pickle
import socket
import threading
import pickle

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.2', 1666))
tuple = (1, 2)
counter = 0
serial = pickle.dumps(tuple)


# Listening to Server and Sending Nickname
def receive():
    while True:
        #print('message')
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024)
            message = pickle.loads(message)
            #message = client.recv(1024).decode('ascii')
            print('Server: ', message)
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            #client.close()
            #break


# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        #print(message)
        client.send(serial)





# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

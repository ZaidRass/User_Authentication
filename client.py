import socket
# Enter the desired IP address
SERVER_IP = 'xxxxxxxx'
SERVER_PORT = 5678

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
    data = s.recv(1024)
    print(data.decode())

    #To let the user enter the message type
    message_type= input('Please enter your message type, 1 for Login and 2 for sign up: ')
    #s.send(message_type.encode())

    # Send the username
    username = input('Please enter your username: ')
    #s.send(username.encode())

    # Send the password
    password = input('Please enter your password: ')
    #s.send(password.encode())
    
    
    Sent_msg = f"{message_type}:{username}:{password}"
    s.send(Sent_msg.encode())

    msg =s.recv(1024).decode()
    print(msg)
    
    #print(s.recv(1024).decode())

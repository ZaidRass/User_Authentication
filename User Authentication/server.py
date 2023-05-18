import socket
import secrets
import hashlib
import csv
import os
import pandas as pd
import numpy as np

#Enter desired IP address
SERVER_IP = 'XXXXXXX'
SERVER_PORT = 5678

def create_CSV_File():
    with open('Login Credentials.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username','HashedPass','Salt'])
       

def Write_credentials(Username, Hashed_Password, Salt):
    with open('Login Credentials.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Username, Hashed_Password, Salt])

def SHA512(Password):
    return hashlib.sha512(Password.encode()).hexdigest()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((SERVER_IP, SERVER_PORT))
    
    print('Server is listening')
    
    s.listen(1)
    
    conn, addr = s.accept()
    
    print(f'Connection accepted from: {addr}')
    
    with conn:
        Username= ''
        Password= ''
        
        # To check if the CSV file is already created or not
        file_exists = os.path.exists('Login Credentials.csv')
        
        # If it doesn't exist, then create it
        if file_exists == False:
            create_CSV_File()    
            
        # To check that the connection has worked
        conn.send(b'Hello World')
        
        # Receive the username,password and the message type from the client
        received_msg = conn.recv(1024).decode()
        message_type, username, password =received_msg.split(':')

        # Signing up
        if message_type == '2':
            # Read the CSV file
            Login_Credentials = pd.read_csv('Login Credentials.csv')
        
        # check if the username already exists
            if username in Login_Credentials['Username'].values:
                s.send(b'The username already exists. Try logging in instead')
            else:
                # Generate the salt
                salt = secrets.token_hex()
                # Add the salt to the password
                salt_password = password + salt
                # Hash the salted password
                hashed_password = SHA512(salt_password)
                # Write the hashed password inside the CSV file
                Write_credentials(username, hashed_password, salt)
                s.send(b'You have successfully signed up')
        
        # Logging in
        if message_type == '1' :
            Login_Credentials = pd.read_csv('Login Credentials.csv')

            # check if the username exists and password matches
            if (Login_Credentials['Username'] == username).any():

                row = Login_Credentials.loc[Login_Credentials['Username'] == username]
                
                hashed_password = row['HashedPass'].values[0]

                salt = row['Salt'].values[0]
                
                salt_password = password + salt
                
                comparable = SHA512(salt_password)
                
                # If the password matches then
                if comparable == hashed_password:
                    s.send(b'You have successfully logged in')
                else:
                    s.send(b'You have entered the wrong password')
            else:
                s.send(b'The username does not exist')
        

        conn.close()

from distutils.command.config import config
from http import server
from operator import is_
import socket
import bcrypt
import json

class OPC_SERVER_SECURITY:
    def __init__(self):
        self.server_socket = socket.socket()
        self.salt = bcrypt.gensalt()
    
    def init_opc_server_security(self, ip):
        self.server_socket.bind((ip, 5000))
        self.server_socket.listen(1)

    def set_server_credentials(self, username, password):
        pwd = password.encode('utf-8')
        user = username.encode('utf-8')
        server_hash_pws = bcrypt.hashpw(pwd, self.salt)
        server_hash_user = bcrypt.hashpw(user, self.salt)

        out_json = dict()

        out_json['username'] = server_hash_user.decode()
        out_json['password'] = server_hash_pws.decode()
        out_json['salt'] = self.salt.decode()

        with open('lab/security/credentials.json', 'w') as fp:
            json.dump(out_json, fp, indent=4, ensure_ascii=False)

    def client_authentication(self):
        config_file = open('credentials.json')
        config_data = json.load(config_file)
        config_file.close()

        is_client_authenticated = False

        print("Waiting for client....")
        conn, address = self.server_socket.accept()

        while True:
            recvd_data = conn.recv(1024).decode()
            recvd_data = recvd_data.split(",")
            user = recvd_data[0]
            pwd = recvd_data[1]
            password = pwd.encode('utf-8')
            username = user.encode('utf-8')
            saved_salt = config_data['salt'].encode('utf-8')
            hashed_pwd = bcrypt.hashpw(password, saved_salt).decode()
            hashed_user = bcrypt.hashpw(username, saved_salt).decode()

            if hashed_user == config_data['username'] and hashed_pwd == config_data['password']:
                conn.send("Success".encode())
                is_client_authenticated = True
            else:
                conn.send("Failure".encode())
                is_client_authenticated = False
                break
        
        if is_client_authenticated:
            print("Server access granted")
            return True
        else:
            print("Server access denied")
            return False
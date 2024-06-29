import unittest
import socket
import threading
from pathlib import Path
import time
from server import StringSearchServer

BASE_DIR = Path(__file__).resolve().parent.parent

class TestStringSearchServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up server in a separate thread.
        """
        config_path = BASE_DIR / 'config' / 'server_config.ini'
        cls.server = StringSearchServer(str(config_path))
        cls.server_thread = threading.Thread(target=cls.server.start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start() 
        time.sleep(1)

    def test_server_existing_string(self):
        """
        Test for a existing string.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 44445))
            query = '3;0;1;28;0;7;5;0;'
            client_socket.sendall(query.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Query: {query} | Server response: {response}")
            self.assertEqual(response.strip(), 'STRING EXISTS')

    def test_server_not_found_string(self):
        """
        Test for 'NOT FOUND' string.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 44445))
            query = 'This is a string that will not be found'
            client_socket.sendall(query.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Query: {query} | Server response: {response}")
            self.assertEqual(response.strip(), 'STRING NOT FOUND')

if __name__ == '__main__':
    unittest.main()

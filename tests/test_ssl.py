import unittest
import socket
import ssl
import threading
import time
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'Server'))

from server import StringSearchServer

class TestSSLStringSearchServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the server with SSL in a separate thread."""
        config_path = BASE_DIR / 'config' / 'server_config.ini'
        cls.server = StringSearchServer(str(config_path))
        cls.server_thread = threading.Thread(target=cls.server.start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)  # Give the server time to start

    def setUp(self):
        """Set up SSL context for the client."""
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def test_ssl_connection_existing_string(self):
        """Test SSL connection for an existing string."""
        with socket.create_connection(('localhost', 44445)) as sock:
            with self.ssl_context.wrap_socket(sock, server_hostname='localhost') as ssock:
                query = '3;0;1;28;0;7;5;0;'
                ssock.sendall(query.encode('utf-8'))
                response = ssock.recv(1024).decode('utf-8')
                self.assertEqual(response.strip(), 'STRING EXISTS')

    def test_ssl_connection_not_found_string(self):
        """Test SSL connection for a non-existing string."""
        with socket.create_connection(('localhost', 44445)) as sock:
            with self.ssl_context.wrap_socket(sock, server_hostname='localhost') as ssock:
                query = 'This is a string that will not be found'
                ssock.sendall(query.encode('utf-8'))
                response = ssock.recv(1024).decode('utf-8')
                self.assertEqual(response.strip(), 'STRING NOT FOUND')

    @classmethod
    def tearDownClass(cls):
        """Stop the server after tests."""
        port = 44445
        try:
            # Attempt to find and kill the process running on the specified port
            import subprocess
            result = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
            if result:
                for line in result.strip().split('\n'):
                    parts = line.split()
                    if len(parts) >= 5 and parts[3].endswith(f':{port}'):
                        pid = parts[4]
                        subprocess.call(f'taskkill /PID {pid} /F', shell=True)
        except subprocess.CalledProcessError:
            print(f"No process found running on port {port}")

if __name__ == '__main__':
    unittest.main()

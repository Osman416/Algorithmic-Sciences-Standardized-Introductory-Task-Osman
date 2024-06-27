import socket
import threading
import ssl
import logging
import time
import configparser
from pathlib import Path

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure logging
log_file_path = BASE_DIR / 'logs' / 'server.log'
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(message)s')

class StringSearchServer:
    """
    A server that searches for strings in 200k.txt file
    
    Returns: 'STRING EXISTS' or 'STRING NOT FOUND'
    
    """
    def __init__(self, config_path: str):
        """
        Initialize the server
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.host = '0.0.0.0'
        self.port = int(self.config['DEFAULT']['Port'])
        self.file_path = BASE_DIR / self.config['DEFAULT']['linuxpath']
        self.reread_on_query = self.config['DEFAULT'].getboolean('REREAD_ON_QUERY')
        self.ssl_enabled = self.config['SSL'].getboolean('enabled')
        self.ssl_context = None
        
        if self.ssl_enabled:
            certfile_path = self.config['SSL']['certfile']
            keyfile_path = self.config['SSL']['keyfile']
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)


    def start_server(self):
        """Start the server & listen for connections"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logging.info(f'Server started on {self.host}:{self.port}')
            while True:
                conn, addr = server_socket.accept()
                if self.ssl_enabled:
                    conn = self.ssl_context.wrap_socket(conn, server_side=True)
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        """Handle client connections."""
        try:
            data = conn.recv(1024).strip(b'\x00').decode('utf-8')
            start_time = time.time()
            logging.debug(f'Received query: {data} from {addr}')
            if self.search_string_in_file(data):
                response = "STRING EXISTS\n"
            else:
                response = "STRING NOT FOUND\n"
            conn.sendall(response.encode('utf-8'))
            exec_time = time.time() - start_time
            logging.debug(f'Execution time: {exec_time:.6f} seconds')
            logging.debug(f'Search result sent to {addr}')
        except Exception as e:
            logging.error(f'Error handling client {addr}: {e}')
        finally:
            conn.close()

    def search_string_in_file(self, query: str) -> bool:
        """
        Search for the query string in the file.

        Args:
            query (str):  query/string to search in 200k.txt file.

        Returns:
            bool: True if 'STRING EXISTS', False if 'STRING NOT FOUND'
        """
        if not self.reread_on_query:
            if not hasattr(self, 'file_content'):
                with open(self.file_path, 'r') as file:
                    self.file_content = file.readlines()
            return query + '\n' in self.file_content
        else:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if query == line.strip():
                        return True
            return False

if __name__ == '__main__':
    config_path = BASE_DIR / 'config' / 'server_config.ini'
    server = StringSearchServer(config_path)
    
    # Print the server IP address (just checking)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Server is running on {ip_address}")
    
    server.start_server()

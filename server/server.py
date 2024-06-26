import socket
import threading
import ssl
import logging
import time

# Configure logging
logging.basicConfig(filename='./logs/server.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

class StringSearchServer:
    """
    A server that searches for strings in 200k.txt file
    
    Returns: 'STRING EXISTS' or 'STRING NOT FOUND'
    
    """
    def __init__(self):
        """
        Initialize the server
        """
        self.host = '0.0.0.0'
        self.port = 44445
        self.file_path = '/data/200k.txt'
        self.reread_on_query = True
        self.ssl_enabled = False

        # CREATE SSL CERT & KEY FILES USING OPENSSL!!!
        """         
            if self.ssl_enabled:
            certfile_path = './test_cert.pem' 
            keyfile_path = './test_key.pem' 
        """

    def start_server(self):
        """Start the server & listen for connections"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logging.info(f'Server started on {self.host}:{self.port}')
            while True:
                conn, addr = server_socket.accept()
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
    server = StringSearchServer()
    server.start_server()

import socket
import threading
import time
from pathlib import Path
import statistics
import sys
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'Server'))

from server import StringSearchServer

def start_server():
    """
    Read the Config file & Start the server.
    """
    config_path = BASE_DIR / 'config' / 'server_config.ini'
    server = StringSearchServer(str(config_path))
    server.start_server()

def stop_server(port):
    """
    Stop the server, using netstat and taskkill to find and kill the process on Windows.
    """
    try:
        # Find the process ID (PID) using the specified port
        result = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
        if result:
            lines = result.strip().split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 5 and parts[3].endswith(f':{port}'):
                    pid = parts[4]
                    # Kill the process using the PID
                    subprocess.call(f'taskkill /PID {pid} /F', shell=True)
                    print(f"Killed process {pid} using port {port}")
    except subprocess.CalledProcessError:
        print(f"No process found running on port {port}")

def is_port_in_use(port):
    """
    Check if the port is in use
    Args:
        port (int): port number to check
        
    Returns:
        bool: True if the port is in use, False if not in use
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def send_query_to_server(server_host: str, server_port: int, query: str) -> str:
    """
    Send a query and return the response
    Args:
        server_host (str)
        server_port (int)
        query (str): query string to send to the server.

    Returns:
        str: Server response to the query.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        client_socket.sendall(query.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        return response.strip()

def run_speed_test(file_sizes, query_counts):
    """
    Run the speed test for various file sizes and query counts.
    Args:
        file_sizes (list): List of file sizes to test.
        query_counts (list): List of query counts to test.

    Returns:
        list: contains file size, query count, and average response time.
    """
    results = []
    port = 44445

    for file_size in file_sizes:
        config_path = BASE_DIR / 'config' / 'server_config.ini'
        with open(config_path, 'w') as config_file:
            config_file.write(f"[DEFAULT]\nPort = {port}\nlinuxpath = data/{file_size}k.txt\nREREAD_ON_QUERY = True\n")
            config_file.write("[SSL]\nenabled = False\ncertfile = ./test_cert.pem\nkeyfile = ./test_key.pem\n")
        
        # see if port is available before starting server
        while is_port_in_use(port):
            print(f"Port {port} is still in use. waiting...")
            time.sleep(2)  # Wait for 2 seconds before checking again

        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()
        time.sleep(2)  # Wait for 2 seconds, time to start

        for query_count in query_counts:
            query_times = []
            for _ in range(query_count):
                start_time = time.time()
                response = send_query_to_server('localhost', port, '3;0;1;28;0;7;5;0;')
                end_time = time.time()
                query_times.append(end_time - start_time)

            avg_time = statistics.mean(query_times)
            results.append((file_size, query_count, avg_time))
            print(f"File size: {file_size}k, Query count: {query_count}, Average time: {avg_time:.6f} seconds")

        stop_server(port) # Stop the server
        time.sleep(3)  # Wait for 2 seconds, to ensure port is closed

    return results

if __name__ == '__main__':
    file_sizes = [10, 50, 100, 200, 500, 1000]  # Different file sizes in kB
    query_counts = [1, 10, 50, 100, 200, 500, 1000]  # Different numbers of queries

    results = run_speed_test(file_sizes, query_counts)

    # Save the results to a text file
    with open(BASE_DIR / 'speed_test_results.txt', 'w') as f:
        for file_size, query_count, avg_time in results:
            f.write(f"File size: {file_size}k, Query count: {query_count}, Average time: {avg_time:.6f} seconds\n")

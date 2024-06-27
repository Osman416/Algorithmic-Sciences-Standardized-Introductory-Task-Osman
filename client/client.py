import socket

def send_query_to_server(server_host: str, server_port: int) -> str:
    """
    Send a query string to the server and return the response.
    Args:op
        server_host (str): The server's host.
        server_port (int): The server's port.
    Returns:
        str: The server's response to the query.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        query = input("Enter your query: ")
        client_socket.sendall(query.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        return response.strip()

if __name__ == '__main__':
    server_host = 'localhost'
    server_port = 44445
    response = send_query_to_server(server_host, server_port)
    print(f'Server response: {response}')

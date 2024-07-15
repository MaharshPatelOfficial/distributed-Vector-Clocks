"""
Description:
This script establishes a client-server connection over TCP/IP and allows the user to input
the number of processes, events per process, and communication lines between processes. It then
sends this information to the server for further processing.

Functions:
- connect_server(address):
  Establishes a TCP connection to the server at the specified address.

- input_process_com_line(client, format):
  Prompts the user to input the number of events for three processes and the number of communication lines.
  Sends this information to the server using the specified format for encoding.

- input_com_info(no_line, format, client):
  Prompts the user to input details for each communication line (sender process, receiver process, sender event,
  receiver event) and sends this information to the server using the specified format.

Usage:
Ensure a server is running and listening on the specified IP address and port (default: localhost, port 1234).
Run this script to establish a connection with the server and provide the required input for process events
and communication lines. The server will receive and process this information accordingly.
"""

import socket

# Function to establish connection with the server
def connect_server(address):
    """
    Establishes a TCP connection to the server at the specified address.

    Parameters:
    - address: Tuple containing IP address and port of the server.

    Returns:
    - client: Socket object representing the client connection.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    print('Client connected to Server')
    return client

# Function to input number of processes and communication lines
def input_process_com_line(client, format):
    """
    Prompts the user to input the number of events for three processes and the number of communication lines.
    Sends this information to the server using the specified format for encoding.

    Parameters:
    - client: Socket object representing the client connection.
    - format: Encoding format (e.g., 'utf-8').

    Returns:
    - no_line: Number of communication lines input by the user.
    """
    no_process1 = input('Event count of process 1:')
    client.send(no_process1.encode(format))

    no_process2 = input('Event count of process 2:')
    client.send(no_process2.encode(format))

    no_process3 = input('Event count of process 3:')
    client.send(no_process3.encode(format))

    no_line = input('communication line count:')
    client.send(no_line.encode(format))

    return no_line

# Function to input communication line information
def input_com_info(no_line, format, client):
    """
    Prompts the user to input details for each communication line (sender process, receiver process,
    sender event, receiver event) and sends this information to the server using the specified format.

    Parameters:
    - no_line: Number of communication lines to input.
    - format: Encoding format (e.g., 'utf-8').
    - client: Socket object representing the client connection.
    """
    i = 0
    while i < no_line:
        sender_process = input('Sender process:')
        client.send(sender_process.encode(format))
        receiver_process = input('Receiver process:')
        client.send(receiver_process.encode(format))
        sender_event_no = input('Sender event:')
        client.send(sender_event_no.encode(format))
        receiver_event_no = input('Receiver event:')
        client.send(receiver_event_no.encode(format))
        i += 1

if __name__ == '__main__':
    # Obtain local IP address and set port
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    format = 'utf-8'

    # Connect to the server
    client = connect_server(address)

    # Input number of communication lines
    no_line = input_process_com_line(client, format)
    no_line = int(no_line)

    # Input communication line details
    input_com_info(no_line, format, client)

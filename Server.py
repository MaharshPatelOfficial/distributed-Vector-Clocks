"""
Description:
This script implements a server-side application that manages vector clocks for three processes
in a distributed system. It listens for client connections, receives input regarding the number of events
for each process and communication lines between processes, and then updates and synchronizes vector clocks
based on messages received from clients.

Functions:
- get_max(x, y):
  Computes the maximum of corresponding elements in vectors x and y.

- initialize_server(address):
  Initializes a TCP socket server and starts listening for incoming connections.

- calculate(no_line, con, size, format, process):
  Handles the logic to update vector clocks based on the communication details received from clients.

- listen_client(server, ip, port, size, format, process):
  Listens for client connections, receives and processes input regarding process events and communication lines,
  and invokes calculate() to update vector clocks accordingly.

Usage:
Ensure this script is running as the server and that clients are configured to connect to the correct IP address
and port (default: localhost, port 1234). Clients should send their process and communication details to the server,
which then updates and prints vector clock values before and after each communication.

Example Run:
Figure 2 : User inputs given for 3 processes and Client connection established
"""

import socket
import random

# Function to compute element-wise maximum of vectors x and y
def get_max(x, y):
    """
    Computes the element-wise maximum of vectors x and y.

    Parameters:
    - x: List representing vector 1.
    - y: List representing vector 2.

    Returns:
    - v: List containing the element-wise maximum of x and y.
    """
    v = [max(value) for value in zip(x, y)]
    return v

# Function to initialize and start the server
def initialize_server(address):
    """
    Initializes a TCP socket server and starts listening for incoming connections.

    Parameters:
    - address: Tuple containing IP address and port number for server binding.

    Returns:
    - server: Socket object representing the server.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen()
    print("Server Started")
    return server

# Function to calculate and update vector clocks
def calculate(no_line, con, size, format, process):
    """
    Handles the logic to update vector clocks based on communication details received from clients.

    Parameters:
    - no_line: Number of communication lines to process.
    - con: Socket connection object with the client.
    - size: Size of data buffer for receiving messages.
    - format: Encoding format (e.g., 'utf-8').
    - process: Dictionary storing vector clock values for each process.
    """
    index = 0
    while index < no_line:
        sender_process = con.recv(size).decode(format)
        sender_process = int(float(sender_process))
        receiver_process = con.recv(size).decode(format)
        receiver_process = int(float(receiver_process))
        sender_event_no = con.recv(size).decode(format)
        sender_event_no = int(float(sender_event_no))
        receiver_event_no = con.recv(size).decode(format)
        receiver_event_no = int(float(receiver_event_no))
        
        print('Sender process:', sender_process, 'Receiver process:', receiver_process, 
              'Sender event:', sender_event_no, 'Receiver event:', receiver_event_no)
        
        # Check validity of sender and receiver process IDs
        if sender_process <= 3 and receiver_process <= 3:
            print(f'P{sender_process} ----> P{receiver_process}')
            
            # Print and update vector clocks based on message receipt
            print(f'Vector clock value of event {sender_event_no} of process {sender_process}: Before: {process[sender_process][sender_event_no]}')
            print(f'Vector clock value of event {receiver_event_no} of process {receiver_process}: Before: {process[receiver_process][receiver_event_no]}')
            
            latest_vector = get_max(process[sender_process][sender_event_no], process[receiver_process][receiver_event_no])
            process[receiver_process][receiver_event_no] = latest_vector
            
            print(f'Vector clock value of event {sender_event_no} of process {sender_process}: After: {process[sender_process][sender_event_no]}')
            print(f'Vector clock value of event {receiver_event_no} of process {receiver_process}: After: {process[receiver_process][receiver_event_no]}')
            
            # Update subsequent vector clocks for the receiver process
            if (receiver_event_no + 1) in process[receiver_process]:
                for i in range(receiver_event_no + 1, len(process[receiver_process]) + 1):
                    process[receiver_process][i] = get_max(process[receiver_process][i - 1], process[receiver_process][i])
        else:
            print("Enter valid values for sender/receiver within existing processes")
        
        index += 1

    print('Final vector value of all processes')
    print(process[1])
    print(process[2])
    print(process[3])

# Function to listen for client connections and handle input reception
def listen_client(server, ip, port, size, format, process):
    """
    Listens for client connections, receives and processes input regarding process events and communication lines,
    and invokes calculate() to update vector clocks accordingly.

    Parameters:
    - server: Socket object representing the server.
    - ip: IP address of the server.
    - port: Port number for server communication.
    - size: Size of data buffer for receiving messages.
    - format: Encoding format (e.g., 'utf-8').
    - process: Dictionary storing vector clock values for each process.
    """
    while True:
        con, address = server.accept()
        print(f'Connected to client - {ip}:{port}')
        
        # Receive and initialize vector clock values for each process
        no_process1 = con.recv(size).decode(format)
        no_process1 = int(no_process1)
        process_event1 = [i for i in range(1, no_process1 + 1)]
        process[1] = {key: [initial_clock + key, 0, 0] for key in process_event1}

        no_process2 = con.recv(size).decode(format)
        no_process2 = int(no_process2)
        process_event2 = [i for i in range(1, no_process2 + 1)]
        process[2] = {key: [0, initial_clock + key, 0] for key in process_event2}

        no_process3 = con.recv(size).decode(format)
        no_process3 = int(no_process3)
        process_event3 = [i for i in range(1, no_process3 + 1)]
        process[3] = {key: [0, 0, initial_clock + key] for key in process_event3}

        print(process[1])
        print(process[2])
        print(process[3])

        # Process communication details and update vector clocks
        no_line = con.recv(size).decode(format)
        no_line = int(no_line)
        calculate(no_line, con, size, format, process)

# Main execution block
if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    port = 1234
    address = (ip, port)
    format = 'utf-8'
    size = 1024
    process = {1: {}, 2: {}, 3: {}}
    initial_clock = 0
    
    # Initialize and start the server
    server = initialize_server(address)
    
    # Listen for client connections and handle communication
    listen_client(server, ip, port, size, format, process)

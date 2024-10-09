#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)

def parse_message(message):
    message = message.decode("utf-8")
    # Parse the application-layer header into the destination SERVER_IP, destination SERVER_PORT,
    # and message to forward to that destination
    SERVER_IP, SERVER_PORT, operation, msg = message.split('|')
    return SERVER_IP, SERVER_PORT, operation, msg

### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.

def main():
    print("server starting - listening for connections at IP", VPN_IP, "and port", VPN_PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as v:
        v.bind((VPN_IP, VPN_PORT))
        v.listen()
        conn, addr = v.accept()
        with conn:
            print(f"Connected established with {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received client message: '{data!r}' [{len(data)} bytes]")

                SERVER_IP, SERVER_PORT, operation, msg = parse_message(data)
                SERVER_PORT = (int)(SERVER_PORT)
                request = f"{operation} {msg}".encode()

                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((SERVER_IP, SERVER_PORT))
                        s.sendall(request)

                        response = s.recv(1024)
                        print(f"Received response from server: '{response.decode()}'")

                    # Forward the server's response back to the client
                    conn.sendall(response)
                    
                except Exception as e:
                    print(f"Error communicating with server: {e}")

print("VPN is done!")

if __name__ == "__main__":
    main()

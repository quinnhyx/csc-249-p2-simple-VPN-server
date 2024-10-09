#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 client.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and print the response')
parser.add_argument('--server_IP', help='IP address at which the server is hosted', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which the server is hosted', **arguments.server_port_arg)
parser.add_argument('--VPN_IP', help='IP address at which the VPN is hosted', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which the VPN is hosted', **arguments.vpn_port_arg)
parser.add_argument('--message', default=['Hello, world'], nargs='+', help='The message to send to the server', metavar='MESSAGE')
args = parser.parse_args()

SERVER_IP = args.server_IP  # The server's IP address
SERVER_PORT = args.server_port  # The port used by the server
VPN_IP = args.VPN_IP  # The server's IP address
VPN_PORT = args.VPN_port  # The port used by the server
MSG = ' '.join(args.message) # The message to send to the server

def encode_message(operation, message):
    # Add an application-layer header to the message that the VPN can use to forward it
    return f"{SERVER_IP}|{SERVER_PORT}|{operation}|{' '.join(map(str, message))}"

def main():
    print("client starting - connecting to VPN at IP", VPN_IP, "and port", VPN_PORT)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((VPN_IP, VPN_PORT))
            operation = input("Enter the operation (concat/reverse): ")
            args = input("Enter words separated by space: ").split()
            request = encode_message(operation, args)
            print(f"connection established, sending message{request}")
            s.sendall(bytes(request, 'utf-8'))
            print("message sent, waiting for reply")
            data = s.recv(1024).decode("utf-8")

        print(f"Received response: '{data}' [{len(data)} bytes]")

    except Exception as e:
            print(f"Error: {e}")
    print("client is done!")

if __name__ == "__main__":
    main()
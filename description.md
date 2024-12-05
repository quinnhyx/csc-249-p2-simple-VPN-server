**Overview of Application**
This application enables communication between a client and a server through a VPN. The client sends requests to the VPN, and VPN forwards these requests to the target server based on the client's message format. The server processes the requests and sends the responses back through the VPN to the client. The application supports two operations: concatenation and reversal of messages.

**Client->VPN Server Message Format**
Messages sent from the client to the VPN server are structured as follows:
<SERVER_IP>|<SERVER_PORT>|<OPERATION>|<MESSAGE>
•	SERVER_IP: The IP address of the target server.
•	SERVER_PORT: The port number on which the target server is listening.
•	OPERATION: The operation to be performed on the message (either "concat" or "reverse").
•	MESSAGE: The actual message content to be processed, with words separated by spaces.
For a message intending to concatenate words at server IP 127.0.0.1 and port 65432, it would look like this:
127.0.0.1|65432|concat|hi cs

**VPN Server->Client Message Format**
The responses sent from the VPN back to the client contain the processed result from the server. The format is simply the raw response from the server, as follows:
<RESPONSE>
Where <RESPONSE> is the result of the requested operation (e.g., the concatenated or reversed message).
If the server concatenates the words "hi" and "cs," the response would be: hics
But in the given echo-server.py, the returned response would be: concat hi cs

**Example Output**
The following is an example of the output in the terminal when running the client, VPN and echo-server:
1.	Client Output:
client starting - connecting to VPN at IP 127.0.0.1 and port 12345
connection established, sending message127.0.0.1|65432|concat hi cs
message sent, waiting for reply
Received response: 'concat hi cs' [12 bytes]      
client is done!
2.	VPN Output:
VPN is done!
server starting - listening for connections at IP 127.0.0.1 and port 12345
Connected established with ('127.0.0.1', 52693)
Received client message: 'b'127.0.0.1|65432|concat hi cs'' [28 bytes]
Received response from server: 'concat hi cs'
3.	Server Output:
server starting - listening for connections at IP 127.0.0.1 and port 65432
Connected established with ('127.0.0.1', 52701)
Received client message: 'b'concat hi cs'' [12 bytes]
echoing 'b'concat hi cs'' back to client
server is done!

**Network Layers Interaction**
1. Client-Side Interactions
***Application Layer***:
The client constructs the message based on user input. This includes selecting the operation (e.g., concatenate or reverse) and preparing the content of the message. The client then uses a socket to send the formatted message to the VPN. This message format includes the server IP, server port, operation, and content, and is transmitted as part of the application protocol. The client sends this data as bytes encoded in UTF-8.
***Transport Layer***:
***Internetwork Layer***:
The client communicates with the VPN over the IP protocol. The client uses the VPN's IP address (as specified by the user) to route packets through the network to the VPN. The IP layer is responsible for addressing, ensuring that the packet reaches the correct VPN.
***Link Layer***:
The client relies on its network interface (Ethernet/Wi-Fi) to transmit the IP packets containing the TCP segments. This layer handles physical addressing (MAC addresses) and frame construction. The link layer facilitates the actual transmission of data over the physical medium (wired or wireless) between the client and the VPN.

2. VPN-Side Interactions
***Application Layer***:
Upon receiving the client's message, the VPN parses the message to extract the target server's IP, port, operation, and message content.
It forwards this data by creating a new socket connection to the actual server, sending the parsed request as a new message.
Once the VPN receives the response from the server, it forwards this response back to the client through the same TCP connection used earlier.
***Transport Layer***:
The VPN maintains two separate TCP connections: One with the client, which is used to receive the initial message and send back the final response. One with the server, which is used to forward the client's request and receive the server's response. The VPN uses TCP for both connections to ensure reliable, ordered transmission of data between the components.
***Internetwork Layer***:
The VPN acts as an intermediary, using IP to route packets both between the client and itself, and between itself and the server.When forwarding a message to the server, the VPN uses the extracted server IP and port from the client's message.
***Link Layer***:
Similar to the client, the VPN relies on its network interface to transmit and receive IP packets. It ensures the physical transmission of data through Ethernet or Wi-Fi between itself, the client, and the server. The VPN ensures that the proper link layer addressing (MAC) is applied to forward the packets.

3. Server-Side Interactions
***Application Layer***:
The server receives the forwarded request from the VPN and processes it based on the operation (concat or reverse) specified in the message. After performing the requested operation, the server prepares a response and sends it back to the VPN. The server behaves as an echo server, receiving the request, processing it, and returning the result.
***Transport Layer***:
The server uses TCP to ensure reliable communication with the VPN. Just like the client, the server establishes a TCP connection with the VPN and uses this connection to receive requests from VPN and send back responses to VPN. TCP guarantees that the message arrives at the VPN without errors and in the correct order.
***Internetwork Layer***:
The server uses the IP protocol to receive the message from the VPN, based on the IP address and port specified in the VPN's request. The IP protocol handles the routing of the VPN's message to the server.
***Link Layer***:
The server's network interface card handles the transmission and reception of IP packets, ensuring that data is physically transmitted through the network infrastructure. This layer facilitates the transfer of data back to the VPN server.

**Command-line trace client and server in operation**
% python echo-client.py --message hello world
client starting - connecting to VPN at IP 127.0.0.1 and port 55554
connection established, sending message127.0.0.1|65432|hello world
message sent, waiting for reply
Received response: 'Invalid operation' [11 bytes]       
client is done!
%python VPN.py
VPN is done!
server starting - listening for connections at IP 
127.0.0.1 and port 55554
Connected established with ('127.0.0.1', 37450)
Received client message: 'b'127.0.0.1|65432|hello 
world'' [27 bytes]
Received response from server: 'Invalid operation'
%python echo-server.py
server starting - listening for connections at IP 
127.0.0.1 and port 65432
Connected established with ('127.0.0.1', 37451)
Received client message: 'b'hello world'' [11 bytes]
echoing 'b'hello world'' back to client
server is done!

**Acknowledgments**
Zhirou and TA Ashley helped to clarify the requirements and debug with the code.

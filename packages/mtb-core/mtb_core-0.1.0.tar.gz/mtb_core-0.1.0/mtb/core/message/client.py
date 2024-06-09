import zmq

context = zmq.Context()

# REQ socket for sending commands and receiving responses
req_socket = context.socket(zmq.REQ)
req_socket.connect("tcp://127.0.0.1:5555")

# SUB socket for subscribing to live output progress
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://127.0.0.1:5556")
sub_socket.subscribe("")  # Subscribe to all messages

# Send a command to the server
command = "Cook"
print(f"Sending command: {command}")
req_socket.send_string(command)

# Poller for multiplexing between the REQ and SUB sockets
poller = zmq.Poller()
poller.register(req_socket, zmq.POLLIN)
poller.register(sub_socket, zmq.POLLIN)

while True:
    socks = dict(poller.poll())

    # Receive live output progress from the server
    if sub_socket in socks:
        progress = sub_socket.recv_string()
        print(progress)

    # Receive the response from the server
    if req_socket in socks:
        response = req_socket.recv_string()
        print(f"Response from server: {response}")
        req_socket.send_string("Quit")
        break

print("Client shutting down")

import time

import msgpack, zmq

context = zmq.Context()

# REP socket for receiving commands and sending responses
rep_socket = context.socket(zmq.REP)
rep_socket.bind("tcp://127.0.0.1:5555")

# PUB socket for streaming live output progress
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://127.0.0.1:5556")

try:
    while True:
        # Receive a command from the client
        msg = rep_socket.recv(0)
        msg = msgpack.unpackb(msg, raw=False)

        print(f"Received command: {msg}")

        if msg == "Quit":
            break

        # Simulate processing the command with live progress updates
        for progress in range(0, 101, 10):
            pub_socket.send(msgpack.packb(f"{{progress: {progress}}}"))
            time.sleep(0.5)

        # Send the response to the client
        rep_socket.send(msgpack.packb("Command completed"))

except KeyboardInterrupt:
    print("Keyboard interrupt received")
finally:
    print("Server shutting down")

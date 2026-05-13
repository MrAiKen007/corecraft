import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:28332")

socket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
socket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
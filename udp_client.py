import cv2
import socket
import math
import pickle
import sys

import numpy as np

max_length = 65000
host = sys.argv[1]
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while ret:
    # compress frame
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()


        # Display the image on the client side
        frame = np.frombuffer(buffer, dtype=np.uint8)
        frame = frame.reshape(frame.shape[0], 1)

        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.flip(frame, 1)
        
        if frame is not None and type(frame) == np.ndarray:
            cv2.imshow("Sender", frame)
            if cv2.waitKey(1) == 27:
                break



        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)

        frame_info = {"packs":num_of_packs}

        # send the number of packs to be expected
        print("Number of packs:", num_of_packs)
        sock.sendto(pickle.dumps(frame_info), (host, port))
        
        left = 0
        right = max_length

        for i in range(num_of_packs):
            print("left:", left)
            print("right:", right)

            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length

            # send the frames accordingly
            sock.sendto(data, (host, port))
    
    ret, frame = cap.read()

print("done")

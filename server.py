import pickle
from datetime import datetime

import time
import face_recognition
import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12121))
server_socket.listen(1)

print("等待客户端连接...")

process_time = time.time()
while time.time() - process_time < 60:
    print(time.time() - process_time)
    client_socket, client_address = server_socket.accept()
    print("客户端已连接:", client_address)

    data_len = int.from_bytes(client_socket.recv(4), 'big')

    data = bytearray()
    while len(data) < data_len:
        packet = client_socket.recv(data_len - len(data))
        if not packet:
            break
        data.extend(packet)

    image_data = pickle.loads(data)
    face_recognitions = []
    face_pixels = []
    start_time = datetime.now()
    for image in image_data:
        print(image.shape[:2])
        face_location = face_recognition.face_locations(image, number_of_times_to_upsample=3)
        face_recognitions.append(face_location)
        top, right, bottom, left = face_location[0]
        face_pixel = (top, right, bottom, left)
        print(face_pixel)
        face_pixels.append(face_pixel)
    end_time = datetime.now()
    execution_time = end_time - start_time
    execution_time = execution_time.seconds + execution_time.microseconds / 1000000

    print(f"Face recognition time: {execution_time}s")
    # 序列化整个列表为 JSON 字符串
    serialized_data = json.dumps(face_pixels)
    # 将 JSON 字符串编码为字节串
    serialized_data_bytes = serialized_data.encode('utf-8')
    client_socket.sendall(serialized_data_bytes)
    client_socket.close()
server_socket.close()
import os
import pickle

import face_recognition
import socket
import json
from PIL import Image
from datetime import datetime


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '172.20.10.12'
server_port = 12121
client_socket.connect((server_host, server_port))

# 记录开始时间
start_time = datetime.now()

image_paths = os.listdir('res')
image_list = []
for image_name in image_paths:
    # 计算部分
    image = face_recognition.load_image_file(f"res/{image_name}")
    (h, w) = image.shape[:2]
    print(f"Image shape: {image.shape}")
    image_list.append(image)
# 记录结束时间
end_time = datetime.now()
# 计算时间差
execution_time = end_time - start_time
print(f"Load image time: {execution_time}")

# 发送数据
serialized_data = pickle.dumps(image_list)
client_socket.sendall(len(serialized_data).to_bytes(4, 'big'))
client_socket.sendall(serialized_data)

# 接收数据
data = bytearray()
while True:
    packet = client_socket.recv(1024)
    if not packet:
        break
    data.extend(packet)

received_data_str = data.decode('utf-8')

face_locations = json.loads(received_data_str)

# 记录开始时间
start_time = datetime.now()
for face_location in face_locations:
    top, right, bottom, left = face_location
    print(f"Face location: Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}")
    face_image = image[top:bottom, left:right]
    # 将 NumPy 数组转换为 PIL 图像并显示
    pil_image = Image.fromarray(face_image)
    pil_image.show()
# 记录结束时间
end_time = datetime.now()
# 计算时间差
execution_time = end_time - start_time
execution_time = execution_time.seconds + execution_time.microseconds / 1000000
print(f"cut time: {execution_time}s")

client_socket.close()
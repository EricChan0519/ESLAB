import socket
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

HOST = '0.0.0.0' 
PORT = 65432  

x_data, y_data, z_data = [], [], []

with open('coordinates.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['X', 'Y', 'Z'])

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) 
        s.listen()        
        print(f"Server is listening on {HOST}:{PORT}...")

        conn, addr = s.accept() 
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(b"10001")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                received_data = data.decode('utf-8').strip()
                print(f"Received: {received_data}")

                try:
                    parts = received_data.split(',')
                    x = int(parts[0].split(':')[1].strip().split()[0])
                    y = int(parts[1].split(':')[1].strip().split()[0])  
                    z = int(parts[2].split(':')[1].strip().split()[0]) 

                    with open('coordinates.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([x, y, z])

                    x_data.append(x)
                    y_data.append(y)
                    z_data.append(z)

                except Exception as e:
                    print(f"Error parsing data: {e}")

                conn.sendall(data) 

def animate(i):
    if len(x_data) > 0:
        plt.cla()
        plt.plot(x_data[-50:], label='X')
        plt.plot(y_data[-50:], label='Y')
        plt.plot(z_data[-50:], label='Z')
        plt.xlabel('Time (samples)')
        plt.ylabel('Value')
        plt.title('Real-Time Sensor Data')
        plt.legend(loc='upper right')

fig = plt.figure()
ani = FuncAnimation(fig, animate, interval=100)

server_thread = threading.Thread(target=start_server)
server_thread.start()

plt.show()

# 等待伺服器線程結束
server_thread.join()

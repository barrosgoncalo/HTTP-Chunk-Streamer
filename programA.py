import os
from socket import *
from sys import *

# python3 programA.py serverURL movieName resultsFileName
# ARGS: programA.py serverURL movieName resultsFileName

buffer_size = 1024

if len(argv) != 4:
    print("Error: wrong number of arguments")
    exit(1)

url = argv[1]
movie_name = argv[2]
results_file_name = argv[3]

addr, port = (url.split('/')[2]).split(':')

socket = socket(family=AF_INET, type=SOCK_STREAM)
socket.connect((addr, int(port)))

request = f"GET ./{movie_name}/manifest.txt HTTP/1.0\r\n\r\n"

socket.send(request.encode())

rcvd_data = socket.recv(buffer_size)

HEADER_OFFSET = 6

# manifest.txt file download

data = b'' # tmp variable

while rcvd_data:
    data += rcvd_data
    rcvd_data = socket.recv(buffer_size)

data_str = data.decode()
header_end = data_str.find("\r\n\r\n")

if not header_end:
    print("Invalid HTTP")
    exit(1)

content = data_str[header_end + 4:]
lines = content.split("\n")

with open(results_file_name, "w") as rf:
    num_tracks = int(lines[1])
    num_seg = int(lines[6])
    rf.write(f"{num_tracks}\n{num_seg}\n")
    total = 0

    for t in range(num_tracks):
        for s in range(num_seg):
            total += int(lines[1 + 6 + s].split(" ")[1])
        rf.write(f"{total}\n")



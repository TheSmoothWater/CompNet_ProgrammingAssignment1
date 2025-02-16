import socket
import os
import hashlib  # needed to verify file hash


IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')


def upload_file(server_socket: socket, file_name: str, file_size: int):
    # create a SHA256 object to verify file hash
    # TODO: section 1 step 5 in README.md file
    myHash = hashlib.new('sha256')
    # create a new file to store the received data
    with open(file_name+'.temp', 'wb') as file:
        while True:
            # TODO: section 1 step 7a - 7e in README.md file
            # replace this line with your code for section 1 step 7a - 7e
            data, address = server_socket.recvfrom(BUFFER_SIZE)
            if not data:
                print("We made it out")
                break
            file.write(data)
            myHash.update(data)
            server_socket.sendto(b'received', address)

    # get hash from client to verify
    print("myHash: ", myHash.digest())
    # TODO: section 1 step 8 in README.md file
    data, address = server_socket.recvfrom(BUFFER_SIZE)
    # TODO: section 1 step 9 in README.md file

    if myHash.digest() == data:
        print('Success')
        server_socket.sendto(b'success', address)
    else:
        print('Failed')
        server_socket.sendto(b'failed', address)


def start_server():
    # create a UDP socket and bind it to the specified IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f'Server ready and listening on {IP}:{PORT}')

    try:
        while True:
            # TODO: section 1 step 2 in README.md file
            # expecting an 8-byte byte string for file size followed by file name
            recvBytes, address = server_socket.recvfrom(BUFFER_SIZE)
            print("We received File Name")
            # TODO: section 1 step 3 in README.md file
            file_info = recvBytes.decode().split(",")
            bytesStringBackToBytes = bytes.fromhex(file_info[0][2:-1].replace("\\x", ""))
            file_size = int.from_bytes(bytesStringBackToBytes, byteorder="big")
            file_name = file_info[1]
            # TODO: section 1 step 4 in README.md file
            server_socket.sendto(b'go ahead', address)
            upload_file(server_socket, file_name, file_size)

    except KeyboardInterrupt as ki:
        pass
    except Exception as e:
        # I added \n so this could be a error in codegrade
        print(f'An error occurred while receiving the file:str\n{e}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()

# 127.0.0.1 your code is fine if you get an F just file a case future me.

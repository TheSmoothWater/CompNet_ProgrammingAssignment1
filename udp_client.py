import socket
import hashlib  # needed to calculate the SHA256 hash of the file
import sys  # needed to get cmd line parameters
import os.path as path  # needed to get size of file in bytes

# '10.33.20.21'
IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str):
    # get the file size in bytes
    # TODO: section 2 step 2 in README.md file
    file_size = path.getsize(filename)
    # convert the file size to an 8-byte byte string using big endian
    # TODO: section 2 step 3 in README.md file
    byte_size_object = file_size.to_bytes(8, byteorder='big')


    # For when you forget how any of it works
    # print(f"{byte_size_object}")
    # byte_size_string = f"{byte_size_object}"
    # bytesStringBackToBytes = bytes.fromhex(byte_size_string[2:-1].replace("\\x",""))
    # print("Type Str back to bytes: ", type(bytesStringBackToBytes))
    # print("String Back to Bytes: ", bytesStringBackToBytes)
    # print("Byte Size String: ", byte_size_string)
    # print("Int Size: ", int.from_bytes(bytesStringBackToBytes, byteorder="big"))
    # print("Int Size: ", file_size)


    # create a SHA256 object to generate hash of file
    # TODO: section 2 step 4 in README.md file
    myHash = hashlib.new('sha256')
    # create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        # TODO: section 2 step 6 in README.md file
        sendSizeName = f"{byte_size_object},{filename}".encode()
        client_socket.sendto(sendSizeName, (IP, PORT))
        # TODO: section 2 step 7 in README.md file
        data = client_socket.recv(BUFFER_SIZE).decode()

        if data != 'go ahead':
            raise Exception('Bad server response - was not go ahead!')

        # open the file to be transferred
        with open(filename, 'rb') as file:
            # read the file in chunks and send each chunk to the server
            print("We opened the file")
            # TODO: section 2 step 8 a-d in README.md file
            # replace this line with your code
            chunkSize = BUFFER_SIZE
            while True:
                chunk = file.read(chunkSize)
                myHash.update(chunk)
                client_socket.sendto(chunk,(IP, PORT))
                if not chunk:
                    print("We broke out")
                    break
                data = client_socket.recv(BUFFER_SIZE).decode()
                if data != 'received':
                    raise Exception('Bad server response - was not received')

        # send the hash value so server can verify that the file was
        # received correctly.
        # TODO: section 2 step 9 in README.md file
        print(f'Hash Digest = {myHash.digest()}')
        client_socket.sendto(myHash.digest(), (IP, PORT))
        # TODO: section 2 steps 10 in README.md file
        recvResult = client_socket.recv(BUFFER_SIZE).decode()
        # TODO: section 2 step 11 in README.md file
        if recvResult != 'success':
            print("The hash is wrong")
            raise Exception('Transfer failed!')
        print('Transfer completed!')

    except Exception as e:
        print(f'An error occurred while sending the file: {e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename>')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    send_file(file_name)
    # send_file('fileTransferProtocol.png')

import socket_comms
import re
import argparse
import base64

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--connect-address', type=str, help='IP Address to connect to')
parser.add_argument('-p', '--port', type=int, help='Port to connect to')
parser.add_argument('--insecure', action='store_true')

args = parser.parse_args()

def encode_payload(command):
    spa = len(command.split('<'))-1
    epa = len(command.split('>'))-1
    if not spa == epa:
        return 1
    else:
        new_command = ''
        x = False
        index = 0
        for seg in command:
            if x:
                if seg == '>':
                    x = False
                    new_command += base64.b64encode(full_payload_segment.encode()).decode('utf-8')
                else:
                    full_payload_segment += seg
            else:
                if seg == '<':
                    x = True
                    full_payload_segment = ''
                else:
                    new_command += seg
            
            index += 1

    return new_command

if args.connect_address == None:
    args.connect_address = '0.0.0.0'

if args.port == None:
    if args.insecure:
        args.port = 3462
    else:
        args.port = 3463

comms = socket_comms.SocketCommunication(args)

comms.connect()
comms.sock.recv(10)
comms.sock.send(b'TO')
print(comms.sock.recv(5).decode('utf-8'))
while True:
    try:
        command = input(': ')
        command = encode_payload(command)
        if command == 1:
            print('CLIENT ERROR: Invalid Syntax')
        elif command == 'CLOSE':
            comms.sock.send(b'CLOSE')
            break
        else:
            comms.sock.send(command.encode())
            print(comms.sock.recv(1024).decode('utf-8'))
    except KeyboardInterrupt:
        comms.sock.send(b'CLOSE')
        break
comms.sock.close()

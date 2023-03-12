import socket_comms
import re
import argparse
import base64
import readline
import os

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--connect-address', type=str, help='IP Address to connect to')
parser.add_argument('-p', '--port', type=int, help='Port to connect to')
parser.add_argument('--insecure', action='store_true')
parser.add_argument('mode', type=str, help='Mode to send to the server, either TO or FROM.')
args = parser.parse_args()

args.mode = args.mode.replace('_TELNET', '')

if not args.mode == 'TO' and not args.mode == 'FROM':
    print('Invalid mode')
    exit(1)

if args.mode == 'TO' and os.path.exists('.session_id'):
    print("Either another client is running in the same mode, or it didn't close propertly. If there is no other client running in TO mode, please delete the .session_id file.")
    exit(1)

if args.mode == 'FROM' and not os.path.exists('.session_id'):
    print('There is no TO client running.')

mode = args.mode

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

def isBase64(s:str) -> bool:
    try:
        base64.b64decode(s.encode()).decode('utf-8')
    except Exception:
        return False
    else:
        return True

def decode_payload(command):
    command_split = command.split(' ')
    x = 0
    for seg in command_split:
        if isBase64(seg):
            command_split[x] = '<' + base64.b64decode(seg.encode()).decode('utf-8') + '>'
        x += 1
    return ' '.join(command_split)

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
if mode == 'TO':
    comms.sock.send(b'TO')
    print(comms.sock.recv(5).decode('utf-8'))
    comms.sock.send(b'GET_ID')
    session_id_f = open('.session_id', 'x')
    session_id_f.write(comms.sock.recv(1024).decode('utf-8'))
    session_id_f.close()
    while True:
        try:
            command = input(': ')
            command = encode_payload(command)
            if command == 1:
                print('CLIENT ERROR: Invalid Syntax')
            elif command == 'CLOSE':
                comms.sock.send(b'CLOSE')
                os.remove('.session_id')
                break
            elif command.replace(' ', '') == '':
                pass
            else:
                comms.sock.send(command.encode())
                print('Sent command')
                print(comms.sock.recv(1024).decode('utf-8'))
        except KeyboardInterrupt:
            comms.sock.send(b'CLOSE')
            os.remove('.session_id')
            break
    comms.sock.close()
else:
    comms.sock.send(b'FROM')
    comms.sock.recv(11)
    session_id_f = open('.session_id', 'r')
    session_id = session_id_f.read()
    session_id_f.close()
    comms.sock.send(session_id.encode())
    while True:
        try:
            print(decode_payload(comms.sock.recv(1024).decode('utf-8')))
            comms.sock.send(b'ACK')
        except KeyboardInterrupt:
            comms.sock.close()
            break

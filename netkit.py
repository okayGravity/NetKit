"""Clone of netcat using python"""
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute (cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), # runs command on local OS and handles output
                                     stderr=subprocess.STDOUT)
    return output.decode()

class NetKit:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        try:
            self.socket.connect((self.args.target, self.args.port))
        except Exception as e:
            print(f'Connection failed: {e}')
            sys.exit()
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                # receive data, if no more data, break
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                # print response data and pause for input
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode()) # send input
        except KeyboardInterrupt:
            print("User terminated the session")
            self.socket.close()
            sys.exit()

    # Binds target and port, listen on loop, passes connected socket to the handle method
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"Starting listener on {self.args.target}:{self.args.port}...")
        while True:
            client_socket, _ = self.socket.accept()
            print(f"[+] Accepted connection from client")
            client_thread = threading.Thread(
                    target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while b'\n' not in cmd_buffer: # Check to make sure user sends valid bytes
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode(errors='ignore'))
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    try:
                        client_socket.shutdown(socket.SHUT_RDWR)
                    except:
                        pass # The Socket might already be closed
                    client_socket.close()
                    return

# Main block for handling cml args and calling funcs
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=r""" 
             _   _      _   _  ___ _   
            | \ | | ___| |_| |/ (_) |_ 
            |  \| |/ _ \ __| ' /| | __|
            | |\  |  __/ |_| . \| | |_ 
            |_| \_|\___|\__|_|\_\_|\__|
            a netcat clone using python
            """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
        netkit.py -t 192.168.1.1 -p 1337 # connect to server
        netkit.py -t 192.168.1.1 -p 1337 -l -c # command shell
        netkit.py -t 192.168.1.1 -p 1337 -l -u=test.txt # upload to a file
        netkit.py -t 192.168.1.1 -p 1337 -l -e=\"cat /etc/passwd\" # execute command
        echo 'foo bar' | netkit.py -t 192.168.1.1 -p 135 # echo text to server port 135
        '''))
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP address')
    parser.add_argument('-p', '--port', type=int, default=1337, help='specified port')
    parser.add_argument('-c', '--command', action='store_true', help='execute command')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-u', '--upload', help='upload a file')
    args = parser.parse_args()

    # if no args passed, print Help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    # invoke NetKit with empty string if listening
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    if buffer is None:
        buffer = b''
    else:
        buffer = buffer.encode()

    nk = NetKit(args, buffer)
    nk.run()

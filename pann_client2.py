#client

import socket
import sys
import select

def pann_client():
    if(len(sys.argv) < 3) :
        print 'please write HOST & PORT'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host.'

     
    while 1:

        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

         
        for sock in ready_to_read:

            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(8192)

                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[PANN] '); sys.stdout.flush()
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[PANN] '); sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(pann_client())

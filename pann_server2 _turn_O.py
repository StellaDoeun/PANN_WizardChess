#server

import socket
import sys
import select

HOST = ''
PORT = 7878
RECV_BUFFER = 1024
SOCKET_LIST=[]

attack_state = 'False'
addr = ''

def pann_receiver():


    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.bind((HOST,PORT))
    p.listen(10)

    SOCKET_LIST.append(p)
    print "PANN server started on port " + str(PORT)+"\n"

    count = 1 # count the player in online
    turn = True

    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
                # a new connection request received

            if sock == p: 
                sockfd, addr = p.accept()
                SOCKET_LIST.append(sockfd)
                print 'Pann (%s, %s) connected' % addr
                broadcast(p,sock,"0")#PANN(%s, %s) is online.\n % addr

                if count % 2 == 0:
                    broadcast(p,sock,"55\n")
                    print"Both PANNs are online\n"

                    # turn notification(pann1 first)
                    send_pann1(p,sockfd,"1\n")
                    print"PANN 1 turn."
                    #broadcast(p, sockfd, "Please put the marker the place which is possible to put.\n") #pann1
                    send_pann2(p,sockfd,"2\n")
                    print"PANN 2 Plz wait.."#pann2
                    #attack(p,sockfd, sock)


                count = count + 1




            else:
                # deliever data to peer
                try:
                    d = sock.recv(RECV_BUFFER)
                    if d:
                        broadcast(p,sock,"\r" + d)

                        # turn notification
                        if turn:
                            turn_pann2(p, sockfd)
                            turn = False



                        else:
                            turn_pann1(p, sockfd)
                            turn = True


                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(p, sock, "3")
                        print"3 PANN (%s, %s) is offline\n" % addr
                        count = count-1

                # exception
                except:
                    broadcast(p, sock, "4")
                    print"4 PANN (%s, %s) is offline\n" % addr
                    count = count-1
                    continue










    p.close()

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

def send_pann1(server_socket, sockfd, msg):

    for socket in SOCKET_LIST:

        if socket != server_socket and socket !=sockfd:
            try:
                socket.send(msg)
            except:
                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def send_pann2(server_socket, sockfd, msg):

    for socket in SOCKET_LIST:

        if socket != server_socket and socket == sockfd:
            try:
                socket.send(msg)
            except:
                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def turn_pann1(p,sockfd):

    send_pann1(p, sockfd, "1")  # Your turn. pann1
    # broadcast(p, sockfd, "Please put the marker the place which is possible to put.\n")
    send_pann2(p, sockfd, "2")  # Plz wait..\n pann2
    # attack(p, sockfd,sock)
    print "PANN 1 turn."
    print "PANN 2 Plz wait.."


def turn_pann2(p,sockfd):

    send_pann2(p, sockfd, "1\n")  # Your turn pann2
    # self_msg(p, sockfd, "Please put the marker the place which is possible to put.\n")
    send_pann1(p, sockfd, "2\n")  # Plz wait...\n pann1
    # attack(p, sockfd,sock)
    print "PANN 2 turn."
    print "PANN 1 Plz wait.."


if __name__=="__main__":

    sys.exit(pann_receiver())

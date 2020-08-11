#server

import socket
import sys
import select

HOST = '127.0.0.1'
PORT = 7779
RECV_BUFFER = 8192
SOCKET_LIST=[]

global attack_state

def pann_receiver():

    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.bind((HOST,PORT))
    p.listen(2)

    SOCKET_LIST.append(p)
    print "PANN server started on port " + str(PORT)+"\n"

    count = 1
    turn = 1

    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
                # a new connection request received

            if sock == p: 
                sockfd, addr = p.accept()
                SOCKET_LIST.append(sockfd)
                print 'Pann (%s, %s) connected' % addr
                broadcast(p,sockfd,"PANN(%s, %s) is online.\n" % addr)

                if count % 2 == 0:
                    notice(p,sock,"Both PANNs are online\n")

                    # turn notification(repeat)
                    broadcast(p,sockfd,"Your turn. ")
                    broadcast(p, sockfd, "Please put the marker the place which is possible to put.\n")
                    self_msg(p,sockfd,"Plz wait..\n")
                    attack(p,sock)

                count = count + 1




            while attack_state == False:

            # deliever data to peer
                try:
                    d = sock.recv(RECV_BUFFER)
                    if d:
                        broadcast(p,sock,"\r"+"PANN"+"["+str(sock.getpeername()) + "]" + d)
                        turn +=1
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(p, sock, "PANN (%s, %s) is offline\n" % addr)
                        count = count-1

                    # exception
                except:
                    broadcast(p, sock, "PANN (%s, %s) is offline\n" % addr)
                    count = count-1
                    continue


                # turn notification
                if turn % 2 == 0:
                    self_msg(p, sockfd, "Your turn")
                    self_msg(p, sockfd, "Please put the marker the place which is possible to put.\n")
                    broadcast(p, sockfd, "Plz wait...\n")
                    attack(p, sock)


                else:
                    broadcast(p, sockfd, "Your turn. ")
                    broadcast(p, sockfd, "Please put the marker the place which is possible to put.\n")
                    self_msg(p, sockfd, "Plz wait..\n")
                    attack(p, sock)

            while attack_state == True:
                notice(p,sock,"Attack Mode")


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

# notice information to peer and self
def notice(server_socket, sock, msg):
    for socket in SOCKET_LIST:
        try:
            socket.send(msg)
            #broadcast(server_socket,sock, msg)
        except:
            # broken socket connection
            socket.close()
            # broken socket, remove it
            if socket in SOCKET_LIST:
                SOCKET_LIST.remove(socket)

#send message to self
def self_msg(server_socket, sock, msg):

    for socket in SOCKET_LIST:

        if socket != server_socket and socket == sock:
            try:
                socket.send(msg)
            except:
                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

#defining attack_state
def attack(server_socket, sock):

    broadcast(server_socket, sock, "Do you want to attack? Answer True/False.\n")

    data = sock.recv(RECV_BUFFER)

    if data == "True\n":
        notice(server_socket, sock, "Attack!")
        attack_state= True

    else:
        attack_state = False


if __name__=="__main__":

    sys.exit(pann_receiver())

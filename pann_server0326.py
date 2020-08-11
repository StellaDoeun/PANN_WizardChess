#server

import socket
import sys
import select
import time
HOST = ''
PORT = 7878
RECV_BUFFER = 1024
SOCKET_LIST=[]

attack_state = False
check_mate = False
addr = ''

def pann_receiver():


    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.bind((HOST,PORT))
    p.listen(10)

    SOCKET_LIST.append(p)
    print ("PANN server started on port " + str(PORT)+"\n")

    count = 1 # count the player in online
    turn = True #true: pann1 turn / false: pann2 turn

    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
                # a new connection request received

            if sock == p: 
                sockfd, addr = p.accept()
                SOCKET_LIST.append(sockfd)
                print ('Pann (%s, %s) connected') % addr
                broadcast(p,sock,"1\n")
                time.sleep(1)

                if count % 2 == 0:
                    broadcast(p,sock,"55\n")
                    print("Both PANNs are online\n")

                    # turn notification(pann1 first)
                    send_pann1(p,sockfd,"1")
                    print("PANN 1 turn.\n")

                    send_pann2(p,sockfd,"2")
                    print("PANN 2 Plz wait..\n")#pann2

                count = count + 1




            else:
                try:
                    try:
                # deliever data to peer
                        if turn:
                            d = sock.recv(RECV_BUFFER)  # recieving moving information from client
                            time.sleep(1)

                            position =d # recieve pann1's position, marker Info and attack
                            print("recieve position data from pann1")

                            print(position + '\n')  # show original position

                            time.sleep(1)
                            send_pann2(p, sock, position)
                            print("send data to pann2")


                                # receive if anim_state is ended, if it is ended
                            a = sock.recv(RECV_BUFFER)
                            time.sleep(1)

                            anim = a

                            print(anim + " animation condition ")

                            anim_end = int(anim)  # 111: anim_end


                            if anim_end == 111:
                                    # --------turn change------------
                                time.sleep(3)
                                broadcast(p,sock,"0\n")
                                turn = False
                                print(turn)





                        # ----------turn : PANN 2------------------
                        else:
                        # recieving moving information from client
                           #da = sock.recv(RECV_BUFFER)
                            time.sleep(1)

                            position = "13-16-201-211-0" # recieve pann2's position, marker Info and attack
                            send_pann1(p, sock, position)

                            print("recieve position data from pann2")
                            print(position + '\n')  # show original position

                            # receive if anim_state is ended, if it is ended
                            an = sock.recv(RECV_BUFFER)

                                #time.sleep(1)
                            anim = an
                            anim_end = int(anim)  # 111: anim_end

                            if anim_end == 111:
                                    # --------turn change-------------
                                turn_pann1(p, sock)
                                time.sleep(5)
                                turn = True
                                print(turn)


                    except:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(p, sock, "3")
                        print("3 PANN (%s, %s) is offline\n") % addr
                        count = count-1

                # exception
                except:
                    broadcast(p, sock, "4")
                    print("4 PANN (%s, %s) is offline\n") % addr
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
                time.sleep(1)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def send_pann1(server_socket, sock, msg):

    for socket in SOCKET_LIST:

        if socket != server_socket and socket !=sock:
            try:
                socket.send(msg)
            except:
                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def send_pann2(server_socket, sock, msg):

    for socket in SOCKET_LIST:

        if socket != server_socket and socket == sock:
            try:
                socket.send(msg)
            except:
                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def turn_pann1(p,sock):

    send_pann1(p, sock, "1\n")
    send_pann2(p, sock, "0\n")
    print ("PANN 1 turn.")
    print ("PANN 2 Plz wait..")


def turn_pann2(p,sock):

    #(p, sock, "1\n")
    broadcast(p,sock,"0\n")
    print ("PANN 2 turn.")
    print ("PANN 1 Plz wait..")


if __name__=="__main__":

    sys.exit(pann_receiver())

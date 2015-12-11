#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import commands
import threading


class ChatServer(object):

    MAX_LISTENRER = 1000 #max number of client support

    def __init__(self,port):
        self.server_port = port
        self.server_addr = ('127.0.0.1',port)
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.client_thread_map = {}

        self.is_running = False

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind(self.server_addr)
        self.server_socket.listen(ChatServer.MAX_LISTENRER)

        self.is_running = True

        while self.is_running:

            #receive a request for chatting from client
            client, client_addr = self.server_socket.accept()
            client_addr_str = Util.addr2str(client_addr)

            # start a new thread to handle chat with client
            new_chat_thread = ChatThread(threadName=client_addr_str,clientSocket=client)
            self.client_thread_map[client_addr_str] = new_chat_thread
            new_chat_thread.start()

    """
    stop server
    note:can't guarantee the server can stop at once
    """
    def stop(self):
        self.is_running = False

    """
    resume server if server is stopped now
    note:can't guarantee the server can resume at once
    """
    def resume(self):
        self.is_running = True

    def stop_all_threads(self):
        map(self.stop_thread,self.client_thread_map.values())

    def stop_thread(self,chatThread):
        if chatThread:
            chatThread.stop()


    def __del__(self):
        print "------destory server------"
        if self.server_socket:
            self.server_socket.close()

        self.stop_all_threads() # cancel all chat threads
        print "------destory finished------"





"""
A class extends Thread for chatting
"""
class ChatThread(threading.Thread):

    BUF_SIZE = 1024

    def __init__(self,threadName,clientSocket):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.clientSocket = clientSocket

        self.is_running = False

    def run(self):
        print "starting" + self.threadName
        self.is_running = True
        self.chat()

    def stop(self):
        self.is_running = False

    def chat(self):
        while self.is_running:
            data = self.clientSocket.recv(ChatThread.BUF_SIZE)
            print data
            self.clientSocket.sendall(data)



"""
A Util class for conveniencing some functions
"""
class Util(object):

    @staticmethod
    def addr2str(addr):
        if len(addr) < 2:
            return "null"
        return addr[0] + ":" + str(addr[1])


if __name__ == '__main__':
    print '------start chat server------'
    chat_server = ChatServer(8888)
    chat_server.start()





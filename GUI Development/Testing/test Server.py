import SocketServer
import cPickle as pickle

HOST = 'localhost'
PORT = 6000
Address = (HOST, PORT)

class TestClass:
    def __init__(self):
        self.name = "dogs"


class MyRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print("connected from: ", self.client_address)
        self.data = ""

        for line in self.rfile:
            self.data += line



        constructedObject = pickle.loads(self.data)

        print("name = ", constructedObject.name)

        
tcpServer = SocketServer.TCPServer(Address, MyRequestHandler)
print("waiting for connection")
tcpServer.serve_forever()

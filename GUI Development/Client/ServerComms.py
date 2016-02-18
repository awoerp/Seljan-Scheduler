import socket
from cPickle import dumps, loads
from Command_Codes import codes
import Users
from sys import getsizeof

INITIAL_BUFFER_SIZE = 1024

class ServerComs():
    def __init__(self):
        self.host = "localhost"
        self.port = 6000
        self.serverAddress = (self.host, self.port)


    def RequestUsernameList(self, currentUser):
        Users.userNames = self.Send_RecieveMessage(codes["UsernameListRequest"])

    def Login(self, userName, password):
        return self.Send_RecieveMessage(codes["LoginRequest"], userName, password)

    def CreateWorkOrderRequest(self, newWorkOrder):
        response = self.Send_RecieveMessage(codes["WorkOrderCreationRequest"], newWorkOrder)

        if response == codes["False"]:
            pass

    def RequestCurrentJobs(self):
        return self.Send_RecieveMessage(codes["CurrentWorkOrdersRequest"])











################## Low Level Methods ######################################################

    def SendMessage(self, messageCode, args):
        clientSocket = socket.socket()
        clientSocket.connect(self.serverAddress)
        message = self.ConstructPickledMessage(messageCode, args)
        messageSize = format(len(message), '04x') # the number of characters is the same as the number of Bytes in a message

        clientSocket.send("0x" + messageSize + message)
        return clientSocket

    def RecieveMessage(self, clientSocket, **kargs):

        messageSize = clientSocket.recv(6)
        incommingMessageSize =  int(messageSize, 16)
        serializedResponse = ""
        while len(serializedResponse) < incommingMessageSize:
            serializedResponse += clientSocket.recv(1024)

        return loads(serializedResponse)

    def Send_RecieveMessage(self, messageCode, *args):
        """
        This method will send a serialized message and return the
        response from the server.
        :param message:
        :return <serialized response from server>:
        """
        response = self.RecieveMessage(self.SendMessage(messageCode, args))
        return response

    def ConstructPickledMessage(self, messageCode, args):
        message = []
        if type(messageCode) is str:
            message.append(messageCode)
        else:
            message.append(str(messageCode))

        message.append(Users.currentUser.name)

        for argument in args:
            if type(argument) is str:
                message.append(argument)
            else:
                pickledArg = dumps(argument)
                message.append(pickledArg)

        serializedMessage = dumps(message)
        return serializedMessage































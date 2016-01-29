from SocketServer import (TCPServer as TCP, StreamRequestHandler as SRH)

from Logging import Log
from cPickle import loads
from Command_Codes import codes
import Work_Order
import Users
import Parameters
import ServerFunctions


HOST = "localhost"
PORT = 6000
address = (HOST, PORT)

log = Log()

users = Users.Users()

currentWorkOrders = Work_Order.CurrentWorkOrders()
currentWorkOrders.LoadExistingOrders()

parameters = Parameters.ParameterManager()
parameters.LoadSettings()

serverFunctions = ServerFunctions.ServerFunctions(log, users, parameters, currentWorkOrders)

class RequestHandler(SRH):
    """
    The "handle()" method of this class is used to
    receive and respond to incoming client requests.
    A message will always come in the form of a
    serialized(pickled) array.  This array will always
    contain a command in index "0" of the array.  Most
    of the time it will also contain the user
    who is operating the client in index "1". The rest
    of the array may be filled with various things like
    arguments, objects and other things.

    From there there is more or less as switch statement
    for that "messageCode" so that the server responds
    correctly

    unpickledMessage = ["<messageCode>", "<user>",..."Argument"]
    (Keep in mind that all of the data within the message array is in
     String format (objects and other dataTypes will need to be unpickled))
    """
    def handle(self):

        serverFunctions.SetHandler(self)
        log.NewLine()
        log.WriteToLog("Connection from: " + str(self.client_address))

        self.serializedMessage = self.request.recv(parameters.parameters["MAX_RECEIVE_SIZE"])
        self.message = loads(self.serializedMessage)
        self.messageType = self.message[0]


        # I want to print out the current user if a user has already been
        # established.  A user would not be established if the user has
        # not logged in yet.  In this case self.message[1] would be blank.
        if self.message[1] != "":
            user = self.message[1]
            log.WriteToLog("Connection as: " + user)
        else:
            pass

        # Client is requesting the usernames for all of the users in the system.
        # This will likely be used on the main login screen for the user drop down menu.
        if self.messageType == codes["UsernameListRequest"]:
            serverFunctions.SendUserNameList()

        # Client is requesting user password authentication on login screen.
        # message[2] = <userName>
        # message[3] = <password>
        elif self.messageType == codes["LoginRequest"]:
            userName = self.message[2]
            password = self.message[3]
            serverFunctions.Login(userName, password)

        # Client is requesting the creation of a new work order.
        # message[2] = <WorkOrder Object>
        elif self.messageType == codes["WorkOrderCreationRequest"]:
            serializedNewWorkOrder =  self.message[2]
            serverFunctions.CreateWorkOrder(serializedNewWorkOrder)

        # This method returns the Recieve buffer size which is specified
        # in the parameters file.
        elif self.messageType == codes["BufferSizeRequest"]:
            serverFunctions.SendReceiveBufferSize()


        log.WriteToLog("Session with %s closed" % str(self.client_address))


    def SendMessage(self, message):
        self.wfile.write(message)







server = TCP(address, RequestHandler)
server.serve_forever()
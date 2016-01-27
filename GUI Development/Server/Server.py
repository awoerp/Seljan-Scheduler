from SocketServer import (TCPServer as TCP, StreamRequestHandler as SRH)

from Logging import Log
from cPickle import loads, dumps
from Command_Codes import codes
import Work_Order
import Users



jobNumber = int
maxMessageSize = int

parameters = [jobNumber, maxMessageSize]

parameterFileName = "Parameters.txt"

paramFile = open(parameterFileName, "r")

count = 0
for line in paramFile:
    data = line.split("\t")
    parameters[0] = int(data[0])
    count += 1
del count

paramFile.close()

def UpdateParameters():
    paramFile = open(parameterFileName, 'w')
    for data in parameters:
        paramFile.write(str(data) + "\n")
    paramFile.close()

HOST = "localhost"
PORT = 6000
address = (HOST, PORT)

log = Log()
users = Users.Users()
currentWorkOrders = Work_Order.CurrentWorkOrders()
currentWorkOrders.LoadExistingOrders()

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

        log.NewLine()
        log.WriteToLog("Connection from: " + str(self.client_address))

        self.serializedMessage = self.request.recv(1024)
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
            usernameList = []
            for user in users.users:
                usernameList.append(user.name)

            serializedUserNameList = dumps(usernameList)
            self.SendMessage(serializedUserNameList)
            log.WriteToLog("UserNameList Requested")



        # Client is requesting user password authentication on login screen.
        # message[2] = <userName>
        # message[3] = <password>
        elif self.messageType == codes["LoginRequest"]:
            userName = self.message[2]
            password = self.message[3]

            for user in users.users:
                if user.name == userName:
                    targetedUser = user
                    log.WriteToLog("LoginRequest for %s" % (targetedUser.name))
                    log.WriteToLog("Given Password: %s" % (password))
            if targetedUser.password == password:
                serializedUser = dumps(targetedUser)
                self.SendMessage(serializedUser)
                log.WriteToLog("Login was successful")
            else:
                self.SendMessage(dumps(""))
                log.WriteToLog("Password was incorrect")

        # Client is requesting the creation of a new work order.
        # message[2] = <WorkOrder Object>
        elif self.messageType == codes["WorkOrderCreationRequest"]:
            serializedNewWorkOrder =  self.message[2]
            newWorkOrder = loads(serializedNewWorkOrder)
            newWorkOrder.jobNumber = parameters[0]
            currentWorkOrders.AddWorkOrder(newWorkOrder)
            parameters[0] += 1 # Increase "jobNumber" by 1

            UpdateParameters() # Saves the new job number in ROM



        log.WriteToLog("Session with %s closed" % str(self.client_address))


    def SendMessage(self, message):
        self.wfile.write(message)







server = TCP(address, RequestHandler)
server.serve_forever()
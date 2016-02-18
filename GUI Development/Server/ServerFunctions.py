from cPickle import dumps, loads

from Command_Codes import codes
from time import sleep


class ServerFunctions():
    def __init__(self, log, users, parameters, currentWorkOrders):
        self.handler = None
        self.log = log
        self.users = users
        self.parameters = parameters
        self.currentWorkOrders = currentWorkOrders
        self.delayRatio = 0.1/1000  #delay 0.1 seconds per 5000 characters

    def SendUserNameList(self):
        usernameList = []
        for user in self.users.users:
            usernameList.append(user.name)

        self.Send(usernameList)
        self.log.WriteToLog("UserNameList Requested")

    def Login(self, userName, password):
        for user in self.users.users:
            if user.name == userName:
                targetedUser = user
                self.log.WriteToLog("LoginRequest for %s" % (targetedUser.name))
                self.log.WriteToLog("Given Password: %s" % (password))
        if targetedUser.password == password:

            self.Send(targetedUser)
            self.log.WriteToLog("Login was successful")
        else:
            self.Send("")  # TODO: This should send back a negative response not
            self.log.WriteToLog("Password was incorrect")

    def CreateWorkOrder(self, serializedNewWorkOrder):
        self.log.WriteToLog("Work Order Creation Attempt")
        try:
            newWorkOrder = loads(serializedNewWorkOrder)

            newWorkOrder.jobNumber = self.parameters.parameters["jobNumber"]
            self.currentWorkOrders.AddWorkOrder(newWorkOrder)
            self.parameters.parameters["jobNumber"] += 1 # Increase "jobNumber" by 1
            self.Send(codes["True"])
            self.parameters.UpdateParameters() # Saves the new job number in ROM
            self.log.WriteToLog("Successfully created work order: %s" % str(newWorkOrder.jobNumber))
        except:
            self.log.WriteToLog("Error: Could not create work order")
            self.Send(codes["False"])


    def SendCurrentWorkOrdersMessageSize(self, size):
        self.Send(size)
        self.log.WriteToLog("Current work orders message size request: %s Bytes" % str(size))



    def SendCurrentWorkOrders(self, workOrdersArray):
        self.Send(workOrdersArray)
        self.log.WriteToLog("Current work orders request")


    def SetHandler(self, handler):
        self.handler = handler

    def Send(self, message):
        serializedMessage = dumps(message)
        loads(serializedMessage)
        messageLength = len(serializedMessage)
        messageSize = format(messageLength, '04x')
        print("messageSize = " + messageSize)
        self.handler.SendMessage("0x" + messageSize + serializedMessage)
        print("Message Length = " + str(messageLength))
        print("Delay Time = " + str(self.delayRatio * messageLength))
        sleep(self.delayRatio * messageLength)

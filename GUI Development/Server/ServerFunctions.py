from cPickle import dumps, loads


class ServerFunctions():
    def __init__(self, log, users, parameters, currentWorkOrders):
        self.handler = None
        self.log = log
        self.users = users
        self.parameters = parameters
        self.currentWorkOrders = currentWorkOrders

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
            self.Send("")  # TODO: This should send back a negative response not ""
            self.log.WriteToLog("Password was incorrect")

    def CreateWorkOrder(self, serializedNewWorkOrder):
        newWorkOrder = loads(serializedNewWorkOrder)

        newWorkOrder.jobNumber = self.parameters.parameters["jobNumber"]
        self.currentWorkOrders.AddWorkOrder(newWorkOrder)
        self.parameters.parameters["jobNumber"] += 1 # Increase "jobNumber" by 1

        self.parameters.UpdateParameters() # Saves the new job number in ROM

    def SendReceiveBufferSize(self):
        self.Send(self.parameters.parameters["MAX_RECEIVE_SIZE"])

    def SetHandler(self, handler):
        self.handler = handler

    def Send(self, message):
        serializedMessage = dumps(message)
        self.handler.SendMessage(serializedMessage)
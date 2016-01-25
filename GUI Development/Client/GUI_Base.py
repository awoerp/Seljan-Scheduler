from Tkinter import *
import Users
import Work_Order
from datetime import date, timedelta
from Command_Codes import codes
from cPickle import dumps, loads
import socket


jobNumber = 1928

HOST = "localhost"
PORT = 6000
SERVER_ADDRESS = (HOST, PORT)
BUFF_SIZE = 1024


class E_Screens:
    __slots__ = ("LoginScreen",
                 "CurrentOrdersScreen",
                 "MyOrdersScreen",
                 "CreateOrderScreen",
                 "AdminScreen")
    LoginScreen = 0
    CurrentOrdersScreen = 1
    MyOrdersScreen = 2
    CreateOrderScreen = 3
    AdminScreen = 4


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Seljan Scheduler")

        self.currentUser = Users.User("", Users.E_UserTypes.Blank, "")
        self.currentWorkOrders = []
        
        self.iconbitmap(r"C:\Users\Andy\Desktop\Programs\Python\Seljan-Scheduler\GUI Development\Client\Clarisse.ico")

        # Initializing Top Menu Buttons and the frame that they go in.
        self.topButtons = []
        topButtonFrame = Frame(self)
        self.topButtons.append(Button(topButtonFrame, text="Current Work Orders",
                                      command=lambda: self.EnterScreen(E_Screens.CurrentOrdersScreen)))
        self.topButtons.append(
            Button(topButtonFrame, text="My Work Orders", command=lambda: self.EnterScreen(E_Screens.MyOrdersScreen)))
        self.topButtons.append(Button(topButtonFrame, text="Create Work Order",
                                      command=lambda: self.EnterScreen(E_Screens.CreateOrderScreen)))
        self.topButtons.append(
            Button(topButtonFrame, text="Admin", command=lambda: self.EnterScreen(E_Screens.AdminScreen)))

        # This block of code packs all of the Top Menu Buttons
        # and sets them to disabled so that they will not work
        # when the Application begins on the Login Screen
        for button in self.topButtons:
            button.pack(fill='x', side=LEFT, expand=True)
            button.config(state=DISABLED)
        topButtonFrame.pack(anchor='n', fill='x')

        # Initializing Content Frame
        # the content frame is located below the Top Menu Buttons.
        # The content frame will contain several subframes which
        # correspond to the content for each menu page.  The subframes
        # are stacked on top of one another (they all reside in the same location
        # in the content frame) and will be raised to the top (visible)
        # using the EnterFrame() method
        contentFrame = Frame(self)
        contentFrame.pack(side="top", fill="both", expand=True)
        contentFrame.grid_rowconfigure(0, weight=1)
        contentFrame.grid_columnconfigure(0, weight=1)

        # This block initializes each of the content subframes and places
        # them in the same location in the contentFrame.
        self.frames = []
        for F in (LoginScreen, CurrentJobsScreen, MyOrdersScreen, CreateWOScreen, AdminScreen):
            frame = F(contentFrame, self)
            self.frames.append(frame)
            frame.grid(row=1, column=0, sticky="nsew")

        # Setting the initial screen to be the LoginScreen
        self.ShowFrame(E_Screens.LoginScreen)

        # These method calls make it so that the root window
        # can not shrink smaller than the default window size.
        # This makes it so that widgets will never be omitted
        # in the window because it has become too small.
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

    def EnterScreen(self, screen):
        """
            Method which depresses the current Top Menu Button
            and switches changes the content frame to reflect
            the current screen.
            """
        self.ResetTopButtons()
        self.topButtons[screen - 1].config(relief=SUNKEN)
        self.ShowFrame(screen)

    def ResetTopButtons(self):
        for b in self.topButtons:
            b.config(relief=RAISED)

        if self.currentUser.CreateWorkOrder == False:
            self.topButtons[2].config(state=DISABLED)

        if self.currentUser.Admin == False:
            self.topButtons[3].config(state=DISABLED)

    def ShowFrame(self, screenNumber):
        self.frames[screenNumber].tkraise()

    def SetCurrentUser(self, user):
        self.currentUser = user

    def GetCurrentUser(self):
        return self.currentUser

    def LeaveLoginScreen(self, password, userName, errorLabelText, menuButtonString):
        for i in Users.users:
            if (i.name == userName):
                self.SetCurrentUser(i)

        if self.currentUser is None:
            errorLabelText.set("Please Select a User")

        elif password == "" and self.currentUser is not Users.Dummy:
            errorLabelText.set("Please Enter the Correct Password")
        elif password.get() == self.currentUser.GetPassword():
            for button in self.topButtons:
                button.config(state=NORMAL)
                password.set("")
                menuButtonString.set("Choose A User")
            self.EnterScreen(1)
        else:
            errorLabelText.set("Incorrect Password Entered")
            password.set("")

    def LeaveLoginScreen(self, password, userName, errorLabelText, menuButtonString):

        # The default value for "userName" is "Choose a User"
        # so if this is still the same value, we don't want to
        # send a request to the server.
        if userName == "Choose a User":
            errorLabelText.set("Please Select a User")
        else:
            serializedMessage = self.ConstructPickledMessage(codes["LoginRequest"], userName, password.get())
            serializedResponse = self.Send_RecieveMessage(serializedMessage)

            message = loads(serializedResponse)
            if message != "":
                self.currentUser = message
                for button in self.topButtons:
                    button.config(state=NORMAL)
                self.EnterScreen(1)
            else:
                errorLabelText.set("Incorrect Password Entered")
                password.set("")


    def RequestUsernameList(self):
        message = self.ConstructPickledMessage(codes["UsernameListRequest"])
        serializedResponse = self.Send_RecieveMessage(message)
        Users.userNames = loads(serializedResponse)

    def CreateWorkOrderRequest(self, newWorkOrder):
        message = self.ConstructPickledMessage(codes["WorkOrderCreationRequest"], newWorkOrder)
        serializedResponse = self.Send_RecieveMessage(message)


    def ConstructPickledMessage(self, messageCode, *args):
        message = []
        if type(messageCode) is str:
            message.append(messageCode)
        else:
            message.append(str(messageCode))

        message.append(self.currentUser.name)

        for argument in args:
            if type(argument) is str:
                message.append(argument)
            else:
                pickledArg = dumps(argument)
                message.append(pickledArg)

        serializedMessage = dumps(message)
        return serializedMessage

    def SendMessage(self, message):
        clientSocket = socket.socket()
        clientSocket.connect(SERVER_ADDRESS)
        clientSocket.send(message)
        return clientSocket

    def RecieveMessage(self, clientSocket):
        return clientSocket.recv(BUFF_SIZE)

    def Send_RecieveMessage(self, message):
        """
        This method will send a serialized message and return the
        response from the server.
        :param message:
        :return <serialized response from server>:
        """
        return self.RecieveMessage(self.SendMessage(message))







class CurrentJobsScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Blank Buffer Frame
        Frame(self, height=10).pack()

        Button(self, text="Job1", bd=1).pack()

        Label(self, text="Job1", bd=1).pack()
        Label(self, text="Job1", bd=1).pack()
        Label(self, text="Job1", bd=1).pack()
        Label(self, text="Job1", bd=1).pack()
        Label(self, text="Job1", bd=1).pack()
        Label(self, text="Job1", bd=1).pack()


class MyOrdersScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        Label(self, text="Job2", bd=1).pack()
        Label(self, text="Job2", bd=1).pack()
        Label(self, text="Job2", bd=1).pack()
        Label(self, text="Job2", bd=1).pack()
        Label(self, text="Job2", bd=1).pack()
        Label(self, text="Job2", bd=1).pack()
        Label(self, text="Job2", bd=1).pack()


class CreateWOScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        defaultDueDateDelta = 7
        self.numOfSubFrames = 4

        ##### Standard Info Area ############
        self.creationDate_Day = IntVar(self)
        self.creationDate_Month = IntVar(self)
        self.creationDate_Year = IntVar(self)

        self.dueDate_Day = IntVar(self)
        self.dueDate_Month = IntVar(self)
        self.dueDate_Year = IntVar(self)

        self.quantity = IntVar(self)
        self.quantity.set(1)

        self.jobTitle = StringVar(self)
        self.customer = StringVar(self)
        self.notes = StringVar(self)
        self.customer.set(Work_Order.customers[0])

        creationDate = date.today()
        day = creationDate.day
        month = creationDate.month
        year = creationDate.year

        self.creationDate_Day.set(day)
        self.creationDate_Month.set(month)
        self.creationDate_Year.set(year)

        defaultDueDate = creationDate + timedelta(days=defaultDueDateDelta)

        self.dueDate = defaultDueDate

        self.dueDate_Day.set(defaultDueDate.day)
        self.dueDate_Month.set(defaultDueDate.month)
        self.dueDate_Year.set(defaultDueDate.year)

        standardInfoFrame = Frame(self, pady=3, padx=5)
        titleFrame = Frame(standardInfoFrame)
        dateFrame = Frame(standardInfoFrame)
        dueDateFrame = Frame(dateFrame, padx=4)
        creationDateFrame = Frame(dateFrame, padx=4)
        middleRowFrame = Frame(standardInfoFrame)
        customerFrame = Frame(middleRowFrame)
        quantityFrame = Frame(middleRowFrame)
        notesFrame = Frame(standardInfoFrame)

        Label(titleFrame, text="Job Title:").pack(side=LEFT)
        Entry(titleFrame, textvariable=self.jobTitle).pack(side=LEFT, fill=X, expand=True)

        Label(creationDateFrame, text="Creation Date:").pack(side=LEFT)
        Entry(creationDateFrame, textvariable=self.creationDate_Month, width=2).pack(side=LEFT)
        Label(creationDateFrame, text="/").pack(side=LEFT)
        Entry(creationDateFrame, textvariable=self.creationDate_Day, width=2).pack(side=LEFT)
        Label(creationDateFrame, text="/").pack(side=LEFT)
        Entry(creationDateFrame, textvariable=self.creationDate_Year, width=4).pack(side=LEFT)

        Label(dueDateFrame, text="Due Date:").pack(side=LEFT)
        Entry(dueDateFrame, textvariable=self.dueDate_Month, width=2).pack(side=LEFT)
        Label(dueDateFrame, text="/").pack(side=LEFT)
        Entry(dueDateFrame, textvariable=self.dueDate_Day, width=2).pack(side=LEFT)
        Label(dueDateFrame, text="/").pack(side=LEFT)
        Entry(dueDateFrame, textvariable=self.dueDate_Year, width=4).pack(side=LEFT)

        Label(customerFrame, text="Customer:").pack(side=LEFT)
        OptionMenu(customerFrame, self.customer, *Work_Order.customers).pack(side=LEFT)

        Label(quantityFrame, text="Quantity:").pack(side=LEFT)
        Entry(quantityFrame, textvariable=self.quantity).pack(side=LEFT)

        Label(notesFrame, text="Notes:").pack(side=LEFT)
        Entry(notesFrame, textvariable=self.notes).pack(side=LEFT, fill=X, expand=True)

        creationDateFrame.pack(side=RIGHT)
        dueDateFrame.pack(side=RIGHT)
        titleFrame.pack(fill=X, expand=True)
        dateFrame.pack()
        customerFrame.pack(side=LEFT)
        quantityFrame.pack(side=RIGHT)
        middleRowFrame.pack(fill=X)
        notesFrame.pack(fill=X)
        standardInfoFrame.pack(fill=X, expand=True)

        #########################################################


        ############ Content (Steps) Area  #####################   
        self.dropDownVariables = []

        self.blankFrameFlags = [True] * self.numOfSubFrames
        self.numActiveFrames = 1

        for i in range(self.numOfSubFrames):
            self.dropDownVariables.append(StringVar(self))
            self.dropDownVariables[i].set(Work_Order.jobOptions[0])
            self.dropDownVariables[i].trace("w", self.RaiseSubFrame)

        # The following for loop creates an array of empty arrays
        self.frames = []
        for i in range(self.numOfSubFrames):
            self.frames.append([])

        contentFrame = Frame(self)
        contentFrame.pack(side=LEFT, fill="both", expand=True)

        count = 0
        for i in range(self.numOfSubFrames):
            for F in (CuttingSubScreen,
                      BendingSubScreen,
                      WeldingSubScreen,
                      PowderCoatingSubScreen,
                      BlankSubScreen):
                frame = F(contentFrame, self, count)
                self.frames[i].append(frame)
                frame.grid(row=i, column=0, sticky="nesw")
            count += 1

        self.blankFrameFlags[0] = False
        self.RaiseSubFrame()
        ##########################################################

        controlButtonFrame = Frame(self)
        Button(controlButtonFrame, text="Add Step", command=self.AddStep).pack()
        Button(controlButtonFrame, text="Remove Step", command=self.RemoveStep).pack()
        Label(controlButtonFrame).pack()
        Button(controlButtonFrame, text="Create Work Order", command=self.CreateWorkOrder).pack()
        controlButtonFrame.pack(side=LEFT)

    def RaiseSubFrame(self, *args):
        for i in range(self.numOfSubFrames):
            # We don't want to update the frames which should stay blank
            if self.blankFrameFlags[i] is False:
                frameToShow = Work_Order.jobOptions.index(self.dropDownVariables[i].get())
                self.frames[i][frameToShow].tkraise()
            else:
                # Show the blank Frame
                self.frames[i][len(self.frames[0]) - 1].tkraise()

    def AddStep(self):

        if self.numActiveFrames >= self.numOfSubFrames:
            pass
        else:
            self.numActiveFrames += 1
            for i in range(self.numActiveFrames):
                self.blankFrameFlags[i] = False

            self.RaiseSubFrame()

    def RemoveStep(self):
        if self.numActiveFrames <= 1:
            pass
        else:
            if self.blankFrameFlags[self.numOfSubFrames - 1] == False:
                self.blankFrameFlags[self.numOfSubFrames - 1] = True
            else:
                for i in range(self.numOfSubFrames):
                    if self.blankFrameFlags[i] == True:
                        self.blankFrameFlags[i - 1] = True

            self.numActiveFrames -= 1
            self.RaiseSubFrame()

    def CreateWorkOrder(self):
        newworkOrder = Work_Order.WorkOrder(self, self.controller.currentUser)
        serializedWorkOrder = dumps(newworkOrder)
        self.controller.CreateWorkOrderRequest(serializedWorkOrder)


class CuttingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent, pady=2, bg='black', bd=2)

        self.frameType = Work_Order.jobOptions[0]

        frame = Frame(self)
        self.dropDownText = StringVar(self)
        self.dropDownText.set(Work_Order.jobOptions[0])
        self.dropDownText.trace("w", controller.RaiseSubFrame)

        self.currentMaterial = StringVar(self)
        self.currentThickness = StringVar(self)

        self.currentMaterial.trace('w', self.UpdateThicknessChart)

        self.materialDrop = OptionMenu(frame, self.currentMaterial, *Work_Order.materialDictionary.keys())
        self.thicknessDrop = OptionMenu(frame, self.currentThickness, ' ')

        self.currentMaterial.set('Mild Steel')

        self.materialDrop.pack(side=LEFT)
        self.thicknessDrop.pack(side=LEFT)

        OptionMenu(frame, controller.dropDownVariables[variableIndex], *Work_Order.jobOptions).pack(side=RIGHT, fill=Y)

        self.NoteString = StringVar()
        self.FileLocationString = StringVar()

        notesFrame = Frame(self)
        Label(notesFrame, text="Notes:").pack(side=LEFT)
        Entry(notesFrame, textvariable=self.NoteString).pack(side=LEFT)

        hyperlinkFrame = Frame(self)
        Label(hyperlinkFrame, text="File Location:").pack(side=LEFT)
        Entry(hyperlinkFrame, textvariable=self.FileLocationString).pack(side=LEFT)

        frame.pack(expand=True, fill=X)
        notesFrame.pack(side=LEFT)
        hyperlinkFrame.pack(side=LEFT)

        self.pack(fill=X, expand=True)

    def UpdateThicknessChart(self, *args):
        temp = Work_Order.materialDictionary[self.currentMaterial.get()]
        self.currentThickness.set(temp[0])
        menu = self.thicknessDrop['menu']
        menu.delete(0, 'end')

        for i in temp:
            menu.add_command(label=i, command=lambda thickness=i: self.currentThickness.set(thickness))


class BendingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent, pady=2, bg='red', bd=2)

        self.frameType = Work_Order.jobOptions[1]

        frame = Frame(self)
        self.dropDownText = StringVar(self)
        self.dropDownText.set(Work_Order.jobOptions[0])
        self.dropDownText.trace("w", controller.RaiseSubFrame)

        ##Label(frame, text = "Cutting").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *Work_Order.jobOptions).pack(side=RIGHT, fill=Y)

        self.NoteString = StringVar()
        self.FileLocationString = StringVar()

        notesFrame = Frame(self)
        Label(notesFrame, text="Notes:").pack(side=LEFT)
        Entry(notesFrame, textvariable=self.NoteString).pack(side=LEFT)

        hyperlinkFrame = Frame(self)
        Label(hyperlinkFrame, text="File Location:").pack(side=LEFT)
        Entry(hyperlinkFrame, textvariable=self.FileLocationString).pack(side=LEFT)

        frame.pack(expand=True, fill=X)
        notesFrame.pack(side=LEFT)
        hyperlinkFrame.pack(side=LEFT)


class WeldingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent, pady=2, bg='green', bd=2)

        self.frameType = Work_Order.jobOptions[2]

        frame = Frame(self)
        self.dropDownText = StringVar(self)
        self.dropDownText.set(Work_Order.jobOptions[0])
        self.dropDownText.trace("w", controller.RaiseSubFrame)

        ##Label(frame, text = "Cutting").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *Work_Order.jobOptions).pack(side=RIGHT, fill=Y)

        self.NoteString = StringVar()
        self.FileLocationString = StringVar()

        notesFrame = Frame(self)
        Label(notesFrame, text="Notes:").pack(side=LEFT)
        Entry(notesFrame, textvariable=self.NoteString).pack(side=LEFT)

        hyperlinkFrame = Frame(self)
        Label(hyperlinkFrame, text="File Location:").pack(side=LEFT)
        Entry(hyperlinkFrame, textvariable=self.FileLocationString).pack(side=LEFT)

        frame.pack(expand=True, fill=X)
        notesFrame.pack(side=LEFT)
        hyperlinkFrame.pack(side=LEFT)


class PowderCoatingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent, pady=2, bg='blue', bd=2)

        self.frameType = Work_Order.jobOptions[3]

        frame = Frame(self)
        self.dropDownText = StringVar(self)
        self.dropDownText.set(Work_Order.jobOptions[0])
        self.dropDownText.trace("w", controller.RaiseSubFrame)

        ##Label(frame, text = "Cutting").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *Work_Order.jobOptions).pack(side=RIGHT, fill=Y)

        self.colorSelection = StringVar()
        self.colorSelection.set(Work_Order.powderCoatColors[0])
        self.NoteString = StringVar()
        self.FileLocationString = StringVar()

        colorFrame = Frame(frame)
        Label(colorFrame, text="Color:").pack(side=LEFT)
        OptionMenu(colorFrame, self.colorSelection, *Work_Order.powderCoatColors).pack(side=LEFT)
        colorFrame.pack(side=LEFT)

        notesFrame = Frame(self)
        Label(notesFrame, text="Notes:").pack(side=LEFT)
        Entry(notesFrame, textvariable=self.NoteString).pack(side=LEFT)

        hyperlinkFrame = Frame(self)
        Label(hyperlinkFrame, text="File Location:").pack(side=LEFT)
        Entry(hyperlinkFrame, textvariable=self.FileLocationString).pack(side=LEFT)

        frame.pack(expand=True, fill=X)
        notesFrame.pack(side=LEFT)
        hyperlinkFrame.pack(side=LEFT)


class BlankSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent)


class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        userNameFrame = Frame(self)
        Label(userNameFrame, text="User:").pack(side=LEFT, fill='x', expand=True)

        menuButtonString = StringVar(self)
        menuButtonString.set("Choose a User")

        controller.RequestUsernameList()
        userNames = Users.userNames

        menuButton = OptionMenu(userNameFrame, menuButtonString, *userNames)
        menuButton.pack(side=LEFT, fill='x', expand=True)
        userNameFrame.pack(fill=X)

        passwordFrame = Frame(self)
        Label(passwordFrame, text="Password: ").pack(side=LEFT, expand=1, fill='x')
        password = StringVar()
        Entry(passwordFrame, textvariable=password, show="*").pack(side=LEFT, expand=1, fill='x')

        self.errorLabelText = StringVar()
        self.errorLabelText.set("")

        passwordFrame.pack(fill=X)
        loginButton = Button(self, text="Login",
                             command=lambda: controller.LeaveLoginScreen(password, menuButtonString.get(),
                                                                         self.errorLabelText, menuButtonString))
        loginButton.pack()

        Label(self, textvariable=self.errorLabelText).pack()


class AdminScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

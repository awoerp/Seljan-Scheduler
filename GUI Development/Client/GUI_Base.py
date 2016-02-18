from datetime import date, timedelta
from Tkinter import *

import ServerComms
import Users
import Work_Order


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

serverComms = ServerComms.ServerComs()


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Seljan Scheduler")



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

        self.messageLabel = Label(self, text = "test").pack(expand = True, fill = X)

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

        if Users.currentUser.CreateWorkOrder == False:
            self.topButtons[2].config(state=DISABLED)

        if Users.currentUser.Admin == False:
            self.topButtons[3].config(state=DISABLED)

    def ShowFrame(self, screenNumber):
        self.frames[screenNumber].tkraise()

    def SetCurrentUser(self, user):
        Users.currentUser = user

    def GetCurrentUser(self):
        return Users.currentUser

    def LeaveLoginScreen(self, password, userName, errorLabelText, menuButtonString):

        # The default value for "userName" is "Choose a User"
        # so if this is still the same value, we don't want to
        # send a request to the server.
        if userName == "Choose a User":
            errorLabelText.set("Please Select a User")
        else:
            response = serverComms.Login(userName, password.get())


            if response != "":
                Users.currentUser = response
                for button in self.topButtons:
                    button.config(state=NORMAL)
                self.EnterScreen(1)
                if Users.currentUser.SetPriority:
                    self.frames[1].increasePriorityButton.config(state = NORMAL)
                    self.frames[1].decreasePriorityButton.config(state = NORMAL)
            errorLabelText.set("Incorrect Password Entered")
            password.set("")



class CurrentJobsScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        controller.currentWorkOrders = serverComms.RequestCurrentJobs()

        self.currentStackNumber = 0

        contentFrame  = Frame(self)
        controlFrame  = Frame(self)
        priorityFrame = Frame(controlFrame, bd = 3)
        scrollFrame   = Frame(controlFrame, bd = 3)



        numberOfJobsToDisplay = 6

        # Create empty frames that will contain the work order information
        workOrderFrames = []

        # The first for loop will determine how many frames deep the stack should be.
        # The line with "%" will return True (1) if there is a remainder.
        for frameStack in range((len(controller.currentWorkOrders) / numberOfJobsToDisplay) +
                                        ((len(controller.currentWorkOrders) % numberOfJobsToDisplay) != 0)):
            workOrderFrames.append([])

        stackNumber = 0
        count = 0
        for frameNumber in range(len(controller.currentWorkOrders)):
            workOrderFrames[stackNumber].append(Frame(contentFrame, bg = "black",bd = 2))
            count += 1

            if count == numberOfJobsToDisplay:
                stackNumber += 1
                count = 0

        # Fill the blank frames with work order info
        count = 0
        stackNumber = 0
        for workOrder in controller.currentWorkOrders:
            if count < numberOfJobsToDisplay:
                currentFrame = workOrderFrames[stackNumber][count]
                topRowFrame = Frame(currentFrame)
                bottomRowFrame = Frame(currentFrame)
                subTaskFrame = Frame(bottomRowFrame)
                Label(topRowFrame, text = "Title: %s" % workOrder.jobTitle, anchor = W).pack(side = LEFT, fill = X, expand = True )
                Label(topRowFrame, text = "Creator: %s" % workOrder.requestor.name, anchor = E).pack(side = RIGHT, fill = X, expand = True )
                Label(bottomRowFrame, text = "Job Number: %s" % str(workOrder.jobNumber), anchor = W).pack(side = LEFT, fill = X, expand = True )
                Label(bottomRowFrame, text = "Customer: %s" % workOrder.customer, anchor = W).pack(side = LEFT, fill = X, expand = True )
                Label(bottomRowFrame, text = "Due Date: %s" % workOrder.dueDate, anchor = W).pack(side = LEFT, fill = X, expand = True )

                for step in workOrder.steps:
                    stepLabel = Label(subTaskFrame, bd = 2)
                    if step.stepType == Work_Order.jobOptions[0]:
                        stepLabel.config(text = "C", bg = 'black', fg = 'white', )
                    elif step.stepType == Work_Order.jobOptions[1]:
                        stepLabel.config(text = "B", bg = "red")
                    elif step.stepType == Work_Order.jobOptions[2]:
                        stepLabel.config(text = "W", bg = "green")
                    else:
                        stepLabel.config(text = "P", bg = "blue")

                    stepLabel.pack(side = LEFT)

                subTaskFrame.pack()

                topRowFrame.pack(fill = X, expand = True)
                bottomRowFrame.pack(fill = X, expand = True)
            count += 1

            if count == numberOfJobsToDisplay:
                count = 0
                stackNumber += 1

        count = 0
        stackNumber = 0
        for frameStack in workOrderFrames:
            for frame in frameStack:
                frame.grid(row=count, column=0, sticky = "ew")
                count += 1

            stackNumber += 1
            count = 0

        ##############  Content Frame  #########################





        ##############  Control Frame  #########################
        self.increasePriorityButton = Button(priorityFrame, text=u"\u25B2", bd=1, state = DISABLED)
        self.increasePriorityButton.pack()
        Label(priorityFrame, text = "Priority").pack()
        self.decreasePriorityButton = Button(priorityFrame, text = u"\u25BC", bd=1, state = DISABLED)
        self.decreasePriorityButton.pack()

        Button(scrollFrame, text=u"\u25B2", bd=1).pack()
        Label(scrollFrame, text = "Scroll").pack()
        Button(scrollFrame, text = u"\u25BC", bd=1).pack()


        priorityFrame.pack(side = LEFT)
        scrollFrame.pack(side = LEFT)
        controlFrame.pack(side = RIGHT)
        contentFrame.pack(side = LEFT, expand = True, fill = X)



        def RaiseSubFrame(self, frameStackToRaise):




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
        newworkOrder = Work_Order.WorkOrder(self, Users.currentUser)
        serverComms.CreateWorkOrderRequest(newworkOrder)


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

        serverComms.RequestUsernameList(Users.currentUser)
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

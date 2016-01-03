from Tkinter import *
import Users
import Work_Order as WO
from numpy import zeros

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
            
            self.currentUser = None
            
            # Initiallizing Top Menu Buttons and the frame that they go in.
            self.topButtons = []
            topButtonFrame = Frame(self)
            self.topButtons.append(Button(topButtonFrame, text = "Current Work Orders",   command = lambda: self.EnterScreen(E_Screens.CurrentOrdersScreen)))
            self.topButtons.append(Button(topButtonFrame, text = "My Work Orders",    command = lambda: self.EnterScreen(E_Screens.MyOrdersScreen)))
            self.topButtons.append(Button(topButtonFrame, text = "Create Work Order", command = lambda: self.EnterScreen(E_Screens.CreateOrderScreen)))
            self.topButtons.append(Button(topButtonFrame, text = "Admin", command = lambda: self.EnterScreen(E_Screens.AdminScreen)))
            
            # This block of code packs all of the Top Menu Buttons
            # and sets them to disabled so that they will not work
            # when the Application begins on the Login Screen
            for button in self.topButtons:
                button.pack(fill = 'x',side = LEFT, expand = True)
                button.config(state = DISABLED)
            topButtonFrame.pack(anchor = 'n', fill = 'x')
            
            # Initializing Content Frame
            # the content frame is located below the Top Menu Buttons.
            # The content frame will contain several subframes which
            # correspond to the content for each menu page.  The subframes
            # are stacked on top of one another (they all reside in the same location
            # in the content frame) and will be raised to the top (visible)
            # using the EnterFrame() method
            contentFrame = Frame(self)
            contentFrame.pack(side = "top", fill = "both", expand = True)
            contentFrame.grid_rowconfigure(0, weight = 1)
            contentFrame.grid_columnconfigure(0, weight = 1)
            
            # This block initializes each of the content subframes and places
            # them in the same location in the contentFrame.
            self.frames = []
            for F in (LoginScreen, CurrentJobsScreen, MyOrdersScreen, CreateWOScreen, AdminScreen):
                frame = F(contentFrame, self)
                self.frames.append(frame)
                frame.grid(row = 1, column = 0, sticky = "nsew")
            
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
            self.topButtons[screen - 1].config(relief = SUNKEN)
            self.ShowFrame(screen)
                        
            
        def ResetTopButtons(self):
            for b in self.topButtons:
                b.config(relief = RAISED)
            
            if self.currentUser.CreateWorkOrder == False:
                self.topButtons[2].config(state = DISABLED) 
                       
            if self.currentUser.Admin == False:
                self.topButtons[3].config(state = DISABLED)
                
                
        def ShowFrame(self, screenNumber):
            self.frames[screenNumber].tkraise()
            
        def SetCurrentUser(self, user):
            self.currentUser = user
            
        def GetCurrentUser(self):
            return self.currentUser
                        
        def LeaveLoginScreen(self, password, userName, errorLabelText, menuButtonString):
            for i in Users.users:
                if(i.name == userName):
                    self.SetCurrentUser(i)
                    
            if self.currentUser is None:
                errorLabelText.set("Please Select a User")
                
            elif password == ""  and self.currentUser is not Users.Dummy:
                errorLabelText.set("Please Enter the Correct Password")
            elif password.get() == self.currentUser.GetPassword():
                for button in self.topButtons:
                    button.config(state = NORMAL)
                    password.set("")
                    menuButtonString.set("Choose A User")
                self.EnterScreen(1)
            else:
                errorLabelText.set("Incorrect Password Entered")
                password.set("")
        



class CurrentJobsScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        # Blank Buffer Frame
        Frame(self, height = 10).pack()
        
        
        
        Button(self,text = "Job1", bd = 1).pack()
        
        Label(self,text = "Job1", bd = 1).pack()
        Label(self,text = "Job1", bd = 1).pack()
        Label(self,text = "Job1", bd = 1).pack()
        Label(self,text = "Job1", bd = 1).pack()
        Label(self,text = "Job1", bd = 1).pack()
        Label(self,text = "Job1", bd = 1).pack()
        

class MyOrdersScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        Label(self,text = "Job2", bd = 1).pack()
        Label(self,text = "Job2", bd = 1).pack()
        Label(self,text = "Job2", bd = 1).pack()
        Label(self,text = "Job2", bd = 1).pack()
        Label(self,text = "Job2", bd = 1).pack()
        Label(self,text = "Job2", bd = 1).pack()
        Label(self,text = "Job2", bd = 1).pack()
        

class CreateWOScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.jobOptions = ["Laser/WaterJet", "Bending", "Welding", "Powder Coating"]
        self.numOfSubFrames = 5
        self.dropDownVariables = []
        
        self.blankFrameFlags = [True] * self.numOfSubFrames
        self.numActiveFrames = 1
        
        for i in range(self.numOfSubFrames):
            self.dropDownVariables.append(StringVar(self))
            self.dropDownVariables[i].set(self.jobOptions[0])
            self.dropDownVariables[i].trace("w", self.RaiseSubFrame)
        
        

        #self.frames = [[]] * self.numOfSubFrames
        self.frames = [[],[],[],[],[]]
        contentFrame = Frame(self)
        contentFrame.pack(side = LEFT, fill = "both", expand = True)
        contentFrame.grid_rowconfigure(self.numOfSubFrames, weight = 1)
        contentFrame.grid_columnconfigure(1, weight = 1)
        count = 0
        for i in range(self.numOfSubFrames):
            
            for F in (CuttingSubScreen,
                       BendingSubScreen,
                       WeldingSubScreen,
                       PowderCoatingSubScreen,
                       BlankSubScreen):
                frame = F(contentFrame, self, count)
                self.frames[i].append(frame)
                frame.grid(row = i, column = 0, sticky = "nsew")
            count += 1

        self.blankFrameFlags[0] = False
        self.RaiseSubFrame()
        
        AddStepFrame = Frame(self)        
        Button(AddStepFrame, text = "Add Step", command = self.AddStep).pack()
        Button(AddStepFrame, text = "Remove Step", command = self.RemoveStep).pack()
        AddStepFrame.pack(side = LEFT)
                        
                
    def RaiseSubFrame(self, *args):
        for i in range(self.numOfSubFrames):
            # We don't want to update the frames which should stay blank
            if self.blankFrameFlags[i] is False:
                frameToShow = self.jobOptions.index(self.dropDownVariables[i].get())
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
                    if self.blankFrameFlags[i] == True :
                        self.blankFrameFlags[i-1] = True

            self.numActiveFrames -= 1                   
            self.RaiseSubFrame()
        
        

class CuttingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent)
        
        frame = Frame(self) 
        self.dropDownText = StringVar(self)
        self.dropDownText.set(controller.jobOptions[0])
        self.dropDownText.trace("w", controller.RaiseSubFrame)
              
        
        Label(frame, text = "Cutting").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *controller.jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)

class BendingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent)
        
        frame = Frame(self)        
        
        Label(frame, text = "Bending").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *controller.jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)

class WeldingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent)
        
        frame = Frame(self)        
        
        Label(frame, text = "Welding").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *controller.jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)

class PowderCoatingSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent)
        
        frame = Frame(self)        
        
        Label(frame, text = "Powder Coating").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownVariables[variableIndex], *controller.jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)



class BlankSubScreen(Frame):
    def __init__(self, parent, controller, variableIndex):
        Frame.__init__(self, parent)
        
        
                                    
                
class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.controller = controller
        userNameFrame = Frame(self)
        Label(userNameFrame, text = "User:").pack(side = LEFT, fill = 'x', expand = True)
        
        menuButtonString = StringVar(self)
        menuButtonString.set("Choose a User")
        
        userNames = []
        for i in Users.users:
            userNames.append(i.GetName())
        menuButton = OptionMenu(userNameFrame, menuButtonString, *userNames)
        menuButton.pack(side = LEFT, fill = 'x', expand = True)
        userNameFrame.pack(fill = X)
        
        passwordFrame = Frame(self)
        Label(passwordFrame, text = "Password: ").pack(side = LEFT, expand = 1, fill = 'x')
        password = StringVar()
        Entry(passwordFrame, textvariable = password, show = "*").pack(side = LEFT, expand = 1, fill = 'x')
        
        self.errorLabelText = StringVar()
        self.errorLabelText.set("")        
        
        passwordFrame.pack(fill = X)
        loginButton = Button(self, text = "Login", command = lambda: controller.LeaveLoginScreen(password, menuButtonString.get(), self.errorLabelText, menuButtonString))
        loginButton.pack()
        

        Label(self, textvariable = self.errorLabelText).pack()
        
        
            
class AdminScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        
                      
class JobScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
                                      
        
      
if __name__ == "__main__":
    app = Application()
    app.mainloop()
from Tkinter import *
import time


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Test")
        
        self.dropDownText = StringVar(self)
        self.dropDownText.set(jobOptions[0])
        self.dropDownText.trace("w", self.ChangeFrame)
        
        contentFrame = Frame(self)
        contentFrame.pack(side = "top", fill = "both", expand = True)
        contentFrame.grid_rowconfigure(0, weight = 1)
        contentFrame.grid_columnconfigure(0, weight = 1)
        
        cut = CuttingFrame(contentFrame, self)
        cut.grid(row = 0, column = 0,sticky = "nsew")
        bend = BendingFrame(contentFrame, self)
        bend.grid(row = 0, column = 0,sticky = "nsew")
        weld = WeldingFrame(contentFrame, self)
        weld.grid(row = 0, column = 0, sticky = "nsew")
        
        self.frames = [cut, bend,weld]
        
        
        self.frames[0].tkraise()
        
        
        
        
    def ChangeFrame(self, *args):
        frameToShow = jobOptions.index(self.dropDownText.get())
        print("cats")
        self.frames[frameToShow].tkraise()
        
        




    
    
class CuttingFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        frame = Frame(self)        
        Label(frame, text = "Cutting").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownText, *jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)
        
class BendingFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        frame = Frame(self)        
        
        Label(frame, text = "Bending").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownText, *jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)
        
class WeldingFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        frame = Frame(self)        
        
        Label(frame, text = "Welding").pack(side = LEFT)
        OptionMenu(frame, controller.dropDownText, *jobOptions).pack(side = LEFT)
        frame.pack(fill = X, expand = True)


jobOptions = ["Laser/WaterJet", "Bending", "Welding", "PowerderCoating"]


if __name__ == "__main__":
    app = Application()
    app.mainloop()
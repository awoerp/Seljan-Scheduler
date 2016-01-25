
class E_State():
    __slots__ = ("Scheduled", "In Progress", "Complete")
    Scheduled   = 0
    In_Progress = 1
    Complete    = 2



materialDictionary = {'Mild Steel': ['1 gauge','2 gauge','3 gauge'],
                      'Aluminum': ['4 gauge','5 gauge','6 gauge']}
powderCoatColors = ["01 - Burly Man Orange", "Assorted"]
customers = ["Harvard", "Trek", "Jame","Utility Trailers"]
jobOptions = ["Laser/WaterJet", "Bending", "Welding", "Powder Coating"]

class WorkOrder:
    def __init__(self,
                 controller,
                 requestor):

        # "controller" is the "CreateWOScreen" object which contains
        # all of the information for the new work order. Many of the
        # variables we want are in the form of Tkinter variables, so
        # it is necessary to use the .get() method to return its int
        # or string value.
        self.controller = controller
        self.jobTitle = controller.jobTitle.get()
        self.requestor = requestor
        self.customer = controller.customer.get()
        self.quantity = controller.quantity.get()
        self.note = controller.notes.get()
        self.steps = []
        self.state = E_State.Scheduled


        # This "for loop" will iterate over an array of booleans
        # that correspond to the "BlankSubScreen" (see class)
        # for each of the possible steps. This will append
        # new steps to self.steps when a blank screen is not active
        count = 0
        for possibleStep in controller.blankFrameFlags:
            if not possibleStep:
                stepType = controller.dropDownVariables[count].get()

                # now I need to figure out which frame within each
                # stack of frames is active.

                # stepStack is the stack of frames which occupy a specific
                # step number.
                stepStack = controller.frames[count]
                for frame in stepStack:
                    if frame.frameType == stepType:
                        StepSubScreenObject = frame
                        break

                if  stepType != jobOptions[0]:
                    StepObject = GeneralStep(stepType, StepSubScreenObject)
                    self.steps.append(StepObject)
                else:
                    StepObject = CuttingStep(StepSubScreenObject)
                    self.steps.append(StepObject)

            count += 1




class GeneralStep:
    def __init__(self, stepType, stepObject):
        self.stepType = stepType
        self.notes = stepObject.NoteString
        self.fileLocation = stepObject.FileLocationString

class CuttingStep(GeneralStep):
    """
    This class inherits from "GeneralStep" and adds two additional
    pieces of information that are necessary for the cutting step.
    """
    def __init__(self, stepObject):
        GeneralStep.__init__(self, jobOptions[0], stepObject)
        self.material = stepObject.currentMaterial
        self.thickness = stepObject.currentThickness
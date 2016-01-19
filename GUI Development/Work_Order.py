
class E_State():
    __slots__ = ("Scheduled", "In Progress", "Complete")
    Scheduled   = 0
    In_Progress = 1
    Complete    = 2


class WorkOrder:
    def __init__(self, jobNum, requestor, dueDate, material, fileLocation, description):
        self.jobNumber = jobNum
        self.requestor = requestor
        self.dueDate = dueDate
        self.material = material
        self.fileLocation = fileLocation
        self.description = description
        self.stakeholders = [requestor]
        
    def AddStakholder(self, user):
        self.stakeholder.append(user)
        

materialDictionary = {'Mild Steel': ['1 gauge','2 gauge','3 gauge'],
                       'Aluminum': ['4 gauge','5 gauge','6 gauge']}
                           
                           
powderCoatColors = ["01 - Burly Man Orange", "Assorted"]
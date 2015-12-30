
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
        
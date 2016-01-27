


class E_UserTypes:
    __slots__ = ("Blank", "Operator", "Regular", "Manager", "Admin")

    Blank    = 0
    Operator = 1
    Regular  = 2
    Manager  = 3
    Admin    = 4



class User:
    def __init__(self, name, userType, pw):
        self.name = name
        self.password = pw
        self.userType = userType
        self.createCustomer = False
        self.editWorkMaterials = False
        self.SetPriority = False
        self.CreateWorkOrder = False
        self.ExecuteWorkOrder = False
        self.Admin = False
        
        if(self.userType == E_UserTypes.Blank):
            pass

        elif(self.userType == E_UserTypes.Operator):
            self.ExecuteWorkOrder = True
            
        elif(self.userType == E_UserTypes.Regular):
            self.CreateWorkOrder = True
            self.createCustomer = False
            self.editWorkMaterials = False
            
        elif(self.userType == E_UserTypes.Manager):
            self.SetPriority = True
            self.CreateWorkOrder = True
            self.createCustomer = False
            self.editWorkMaterials = False
        else:
            self.SetPriority = True
            self.CreateWorkOrder = True
            self.ExecuteWorkOrder = True
            self.Admin = True
            self.createCustomer = False
            self.editWorkMaterials = False
            
    def GetPassword(self):
        return self.password
                  
    def GetName(self):
        return self.name

userNames = []

# This should go away once the user functionality on the server is working correctly
"""
Andy  = User("Andy Woerpel", E_UserTypes.Admin, "cats")
Steve = User("Steve Woerpel", E_UserTypes.Operator, "cats")
Scott = User("Scott Woerpel", E_UserTypes.Manager, "cats")
Dummy = User("Dummy", E_UserTypes.Regular, "")

users = [Dummy, Andy, Steve, Scott]
"""
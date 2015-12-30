


class E_UserTypes:
    __slots__ = ("Operator", "Regular", "Manager", "Admin")
    
    Operator = 0
    Regular  = 1
    Manager  = 2
    Admin    = 3



class User:
    def __init__(self, name, userType, pw):
        self.name = name
        self.password = pw
        self.userType = userType
        self.SetPriority = False
        self.CreateWorkOrder = False
        self.ExecuteWorkOrder = False
        self.Admin = False
        
        
        if(self.userType == E_UserTypes.Operator):
            self.ExecuteWorkOrder = True
            
        elif(self.userType == E_UserTypes.Regular):
            self.CreateWorkOrder = True
            
        elif(self.userType == E_UserTypes.Manager):
            self.SetPriority = True
            self.CreateWorkOrder = True
            
        else:
            self.SetPriority = True
            self.CreateWorkOrder = True
            self.ExecuteWorkOrder = True
            self.Admin = True
            
    def GetPassword(self):
        return self.password
                  
    def GetName(self):
        return self.name
        

Andy  = User("Andy Woerpel", E_UserTypes.Admin, "cats")
Steve = User("Steve Woerpel", E_UserTypes.Operator, "cats")
Scott = User("Scott Woerpel", E_UserTypes.Manager, "cats")
Dummy = User("Dummy", E_UserTypes.Regular, "")

users = [Dummy, Andy, Steve, Scott]
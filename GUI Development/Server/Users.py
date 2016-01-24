from cPickle import loads, dumps
from os import getcwd, listdir, chdir

class E_UserTypes:
    __slots__ = ("Operator", "Regular", "Manager", "Admin")

    Operator = 0
    Regular  = 1
    Manager  = 2
    Admin    = 3

userFilesDirectory = r"\\Users"

class Users:
    def __init__(self):
        self.users = []
        self.LoadUsers()


    def LoadUsers(self):
        cwd = getcwd()
        chdir("Users")
        # Each of the Users is stored as a file in the "Users"
        # directory.  This unpickles each of those user objects
        # and appends them to the list of user objects.
        for file in listdir(getcwd()):

            userFile = open(file, 'r')
            serializedUserObject = ""
            for line in userFile:
                serializedUserObject += line
            userObject = loads(serializedUserObject)
            self.users.append(userObject)
            userFile.close()
        chdir(cwd)

    def AddUser(self, newUser):
        self.users.append(newUser)

    def Close(self):
        cwd = getcwd()
        chdir("Users")
        cwd = getcwd()
        for user in self.users:
            userFile = open(user.name + ".txt",'w')
            serializedUser = dumps(user)
            userFile.write(serializedUser)
            userFile.close()


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


        if(self.userType == E_UserTypes.Operator):
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


Andy  = User("Andy Woerpel", E_UserTypes.Admin, "cats")
Steve = User("Steve Woerpel", E_UserTypes.Operator, "cats")
Scott = User("Scott Woerpel", E_UserTypes.Manager, "cats")
Dummy = User("Dummy", E_UserTypes.Regular, "")


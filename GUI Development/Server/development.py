from Users import User, Users, E_UserTypes


allUsers = Users()

Andy  = User("Andy Woerpel", E_UserTypes.Admin, "cats")
Steve = User("Steve Woerpel", E_UserTypes.Operator, "cats")
Scott = User("Scott Woerpel", E_UserTypes.Manager, "cats")
Dummy = User("Dummy", E_UserTypes.Regular, "")
Clide = User("Clide", E_UserTypes.Regular, "")

users = [Dummy, Andy, Steve, Scott]


allUsers.AddUser(Clide)

allUsers.Close()

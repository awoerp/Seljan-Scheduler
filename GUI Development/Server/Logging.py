from datetime import date, datetime
from os import getcwd, chdir

class Log:
    def __init__(self):
        cwd = getcwd()

        self.date = date.today()
        day   = str(self.date.day)
        month = str(self.date.month)
        year  = str(self.date.year)

        chdir("Logs")
        self.logFile = open("ServerLog %s-%s-%s.txt" % (month, day, year), 'a')
        self.WriteToLogWithTimeStamp("Server Stated")
        chdir(cwd)

    def WriteToLogWithTimeStamp(self, body):
        timeStamp = str(datetime.now())
        message = timeStamp + ": " + body + "\n"

        self.logFile.write(message)
        self.logFile.flush()

    def WriteToLog(self, body):
        timeStamp = str(datetime.now())
        message = body + "\n"

        self.logFile.write(message)
        self.logFile.flush()

    def NewLine(self):
        self.logFile.write("\n")
        self.logFile.flush()
    def Close(self):
        self.logFile.close()




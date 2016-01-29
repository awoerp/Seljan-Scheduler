



class ParameterManager():
    def __init__(self):
        self.parameters = {}
        self.paramFilename = "Parameters.txt"

    def LoadSettings(self):
        paramFile = open(self.paramFilename, "r")
        for line in paramFile:
            data = line.split("\t")
            self.parameters[data[1].strip()] = int(data[0])
        paramFile.close()

    def UpdateParameters(self):
        paramFile = open(self.paramFilename, 'w')
        for key in self.parameters:
            paramFile.write(str(self.parameters[key]) + "\t" + key + "\n")
        paramFile.close()
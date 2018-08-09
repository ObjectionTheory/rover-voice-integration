
class Rover:
    def __init__(self, id):
        self.id = id
        self.currentInstruction = None
    
    def updateData(self, data):
        self.currentInstruction = data
        self.postData(self)

    def postData(self):
        return "Rover" + self.id + ":"self.currentInstruction
    
    def selfDestruct(self):
        del self
    
    
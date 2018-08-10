
class Rover:
    def __init__(self, id):
        self.id = id
        self.left = 0
        self.right = 0
        self.duration = 0
    
    def updateData(self, left, right, duration):
        self.left = left
        self.right = right
        self.duration = duration

    def postData(self):
        res = {
            "roverid": self.id,
            "left": self.left,
            "right": self.right,
            "duration": self.duration
        }
        self.left = 0
        self.right = 0
        self.duration = 0

        return res
    
    def selfDestruct(self):
        del self
    
    
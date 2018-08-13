
class Rover:
    def __init__(self, id):
        self.id = id
        self.reset()
    
    def updateData(self, left, right, duration):
        self.left = left
        self.right = right
        self.duration = duration

    def isMoving(self):
        if self.left != 0 and self.right != 0:
            return True
        return False
    
    def reset(self):
        self.left = 0
        self.right = 0
        self.duration = 0

    def postData(self):
        res = {
            "roverid": self.id,
            "left": self.left,
            "right": self.right,
            "duration": self.duration
        }
        self.reset()
        return res
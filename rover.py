
class Rover:
    def __init__(self, id):
        self.id = id
        self.reset()
    
    def updateData(self, left, right, duration, claw):
        self.left = left
        self.right = right
        self.duration = duration
        self.claw = claw

    def isMoving(self):
        if self.left != 0 and self.right != 0:
            return True
        return False
    
    def reset(self):
        self.left = 0
        self.right = 0
        self.duration = 0
        self.claw = 0

    def postData(self, reset=True):
        res = {
            "roverid": self.id,
            "left": self.left,
            "right": self.right,
            "duration": self.duration,
            "claw": self.claw
        }
        if reset:
            self.reset()

        return res
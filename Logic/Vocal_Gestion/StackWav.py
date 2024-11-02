from Logic.Stack import Stack

class StackWav:
    
    stack = None
    
    def __init__(self):
        self.stack = Stack()
        
        
    def getStack(self):
        return self.stack.__str__()
    
    def getLastFromStack(self):
        return self.stack.pop()

    def StackAppend(self,stringWav):
        self.stack.push(stringWav)
        
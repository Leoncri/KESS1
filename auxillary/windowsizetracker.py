class WindowSizeTracker:
    """ class for tracking the window size """
    
    def __init__(self, root, callback):
        # store variables
        self.root = root
        self.callback = callback
        
        self.width = root.winfo_width()
        self.height = root.winfo_height()
        
        # bind the configure callback
        self.root.bind("<Configure>", self.Resize)
    
    def Resize(self, event):
        # check which widget calls
        if (event.widget == self.root):
            if (self.width != event.width) or (self.height != event.height):
                self.width = event.width
                self.height = event.height
                
                # use own callback
                self.callback(self.width, self.height)
        
        return
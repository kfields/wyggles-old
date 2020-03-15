
from layer import Layer

class Renderer():
    
    def __init__(self):
        root = Layer("root")
    
    def render(self):
        self.root.render()
        
    def get_root(self):
        return self.root
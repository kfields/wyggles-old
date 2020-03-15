import operator

class Layer():    
    def __init__(self, name):
        self.name = name
        self.layers = []
        self.sprites = []
    
    def render(self):
        for sprite in self.sprites:
            sprite.render()        
        for layer in self.layers:
            layer.render()
            
    def add_layer(self, layer):
        self.layers.append(layer)
        
    def remove_layer(self, layer):
        self.layers.remove(layer)            
            
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        #depth_sort()
        
    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)
        
    def depth_sort(self):
        self.sprites.sort(key=operator.attrgetter('z'))
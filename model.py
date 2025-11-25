


class Model:
    bodies = []
    
    
    def __init__(self):
        pass
    
    def collisions(self):
        for b in self.bodies:
            b.check_collisions()
            
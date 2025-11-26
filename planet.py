from body import Body

class Planet(Body):
    def __init__(self, pos, vel, mass, radius, model):
        super().__init__(pos, vel, mass, radius, model)
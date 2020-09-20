import random
WIDTH = 400
HEIGHT = 800
SPEED = 4


class Rocket():
    def __init__(self, dna = None, fitness = None):
        if fitness:
            self.fitness = fitness
        else:
            self.fitness = 0
        self.dead = False
        self.completed = False
        self.comp_steps = None
        self.leader = False
        self.h = 10
        self.w = 50
        self.r = 10
        self.path = []
        if dna:
            self.DNA = dna
        else:
            self.DNA = [] 
        self.location = PVector(WIDTH/2,HEIGHT-5)
        self.velocity = PVector(0,0)
        self.acceleration = PVector(0,0)


    def apply_force(self, f):
        self.acceleration.add(f)

    def update(self, curr_step):
        self.apply_force(self.DNA[curr_step])
        self.velocity.add(self.acceleration)
        self.velocity.setMag(SPEED)
        self.location.add(self.velocity)
        self.acceleration.mult(0)
        if self.completed:
            self.comp_steps = curr_step

    def render(self,popsize, target):
        rectMode(CENTER)
        shapeMode(CENTER)
        pushStyle()
        noStroke()
        fill(0,120,255,100)
        if self.leader:
            pushStyle()
            stroke(255,100)
            line(target.loc.x, target.loc.y, self.location.x, self.location.y)
            popStyle()
        pushMatrix()
        translate(self.location.x, self.location.y)
        self.path.append(PVector(self.location.x, self.location.y))
        theta = self.velocity.heading() - PI / 2;
        rotate(theta)
        beginShape()
        vertex(-self.r, 0)
        vertex(0,self.r*3)
        vertex(self.r,0)
        endShape(CLOSE)
        popMatrix()
        if popsize <= 100:
            pushStyle()
            stroke(0,255,255,75)
            for i in self.path:
                point(i.x,i.y)
            popStyle()
        popStyle()

    def collision(self, goal, walls=None):
        if dist(self.location.x, self.location.y, goal.loc.x, goal.loc.y)<15:
            self.completed = True
            self.dead = True
        if walls:
            for wall in walls:
                if(self.location.x > wall.x and self.location.x < wall.x + wall.sx and
                    self.location.y > wall.y and self.location.y-self.r
                    < wall.y + wall.sy):
                    self.dead = True
        if self.location.x < 0:
            self.dead = True
        if self.location.x > WIDTH:
            self.dead = True
        if self.location.y < 0:
            self.dead = True
        if self.location.y > HEIGHT:
            self.dead = True

class Goal():
    def __init__(self, vector):
        self.loc = vector

    def render(self):
        pushStyle()
        noStroke()
        fill(255,0,80)
        ellipse(self.loc.x, self.loc.y, 30,30)
        popStyle()

class Wall():
    def __init__(self,x,y,sz = 75):
        self.x = x
        self.y = y
        self.sx = sz
        self.sy = 10

    def render(self):
        pushStyle()
        rectMode(CORNER)
        fill(120)
        noStroke()
        rect(self.x, self.y, self.sx, self.sy)
        popStyle()

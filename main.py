import objects
import evolution as evo


WIDTH = 400
HEIGHT = 800
popsize = 70
NUMSTEPS = HEIGHT/2

target = PVector(WIDTH/2, 100)
walls = []
begin = False

def setup():
    global e, walls, popsize
    size(WIDTH,HEIGHT)
    e = evo.Evolution(popsize, NUMSTEPS, target)
    createWalls()


def draw():
    global walls, target, e, begin, popsize
    background(0)
    textSize(32)
    text("Generation: "+str(e.num_generations), 10, 30)
    text("Pop Size: "+str(popsize), 10, 60)
    fill(0, 102, 153)
    if keyPressed:
        if key == 's' or key == 'S':
            begin = True
        if key == 'r' or key == 'R':
            restart()
        if key == 'g' or key == 'G':
            target = PVector(mouseX, mouseY)
            e.set_goal(target)
        if (key == CODED):
            if keyCode == UP:
                popsize+=5
                if popsize>500:
                    popsize = 500
                restart()
            if keyCode == DOWN:
                popsize-=5
                if popsize<10:
                    popsize = 10
                restart()
            if keyCode == RIGHT:
                popsize = 500
                restart()
            if keyCode == LEFT:
                popsize = 10
                restart()

    if mousePressed and mouseButton == LEFT:
        walls.append(objects.Wall(mouseX, mouseY))
    if mousePressed and mouseButton == RIGHT:
        if walls:
            walls.pop()

    if begin:
        e.run(walls)

    e.goal.render()
    for wall in walls:
        wall.render()

def createWalls():
    walls.append(objects.Wall((WIDTH/2-WIDTH/8),2*HEIGHT/3 , WIDTH/4))
    walls.append(objects.Wall((WIDTH/2-WIDTH/2),2*HEIGHT/3 , WIDTH/4))
    walls.append(objects.Wall((WIDTH/2+WIDTH/4),2*HEIGHT/3 , WIDTH/4))
    walls.append(objects.Wall((WIDTH/3-WIDTH/12),HEIGHT/3, WIDTH/6))
    walls.append(objects.Wall((WIDTH/3+WIDTH/4),HEIGHT/3, WIDTH/6))

def restart():
    global e, popsize, NUMSTEPS, target, begin
    e = evo.Evolution(popsize, NUMSTEPS, target)
    begin = False



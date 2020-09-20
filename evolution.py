import objects
import random

WIDTH = 400
HEIGHT = 800
TURN_RATE = .3

class Evolution():
    def __init__(self,popsize, num_steps, vector = PVector(200,50)):
        self.goal = objects.Goal(vector)
        self.mutation_rate = .01
        self.curr_step = 0
        self.deadcount = 0
        self.num_steps = num_steps
        self.popsize = popsize
        self.rockets = []
        self.init_population()
        self.num_generations = 1


    def set_goal(self, goalin):
        self.goal = objects.Goal(goalin)

    def init_population(self):
        del self.rockets[:]
        for i in range(self.popsize):
            self.rockets.append(objects.Rocket())
        for rocket in self.rockets:
            for i in range(self.num_steps):
                rocket.DNA.append(PVector.random2D())
                rocket.DNA[i].setMag(TURN_RATE)

    def calc_fitness(self):
        for rocket in self.rockets:
            t = 0
            d = dist(rocket.location.x, rocket.location.y,
                    self.goal.loc.x, self.goal.loc.y)
            if rocket.completed:
                t = self.num_steps/rocket.comp_steps
            d_ = map(d, 0, HEIGHT, 1,0)
            rocket.fitness = (t+d_)**2
            rocket.fitness *= 20
    # def calc_fitness(self):
    #     for rocket in self.rockets:
    #         d = dist(rocket.location.x, rocket.location.y,
    #                 self.goal.loc.x, self.goal.loc.y)
    #         rocket.fitness = map(d, 0, HEIGHT, 1, 0)
    #         if rocket.completed:
    #             rocket.fitness+=map(rocket.comp_steps, 0, self.num_steps, 5,0)
    #             rocket.fitness *= 10
    #         rocket.fitness *= 20

    def curr_fit(self):
        max = 0
        index = 0
        counter = 0
        for rocket in self.rockets:
            rocket.leader = False
            d = dist(rocket.location.x, rocket.location.y,
                    self.goal.loc.x, self.goal.loc.y)
            d = map(d, 0, HEIGHT, 1, 0)
            if d > max:
                max = d
                index = counter
            counter += 1
        self.rockets[index].leader = True

    def selection(self):
        selection_pool = []
        for rocket in self.rockets:
            for i in range(int(rocket.fitness)):
                selection_pool.append(rocket)
        return selection_pool

    def crossover(self, sp):
        parentA = sp[random.randint(0,len(sp)-1)].DNA
        parentB = sp[random.randint(0,len(sp)-1)].DNA
        split = random.randint(0,self.num_steps)
        childDNA = parentA[:split] + parentB[split:]
        childDNA = self.mutation(childDNA)
        return childDNA

    def mutation(self, child):
        new_child = child
        if random.random() < self.mutation_rate:
            for i in range(self.num_steps):
                new_child.append(PVector.random2D())
                new_child[i].setMag(TURN_RATE)
        return new_child

    def new_pop(self):
        new_population = []
        selection_pool = self.selection()
        for i in self.rockets:
            new_population.append(objects.Rocket(self.crossover(selection_pool)))
        for rocket in new_population:
            rocket.DNA = self.crossover(selection_pool)
        self.rockets = new_population

    def evaluate(self):
        if self.curr_step >= self.num_steps or self.deadcount >= len(self.rockets):
            self.curr_step = 0
            self.deadcount = 0
            self.calc_fitness()
            self.new_pop()
            self.num_generations+=1

    def run(self, walls=None):
        self.curr_fit()
        self.goal.render()
        for rocket in self.rockets:
            if not rocket.dead:
                if not rocket.completed:
                    rocket.collision(self.goal, walls)
                    if rocket.dead:
                        self.deadcount += 1
                    rocket.update(self.curr_step)
            rocket.render(self.popsize, self.goal)
        self.curr_step += 1
        self.evaluate()

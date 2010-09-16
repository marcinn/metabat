import random
import math

def calculate_average_loudness(bats):
    return sum((b.loudness for b in bats)) / len(bats)


class Population(object):
    def __init__(self, bats, freq_range, sol, df, a=0.9, g=0.9):
        """
        initialize population of bats
        with specified frequency range (min, max)
        and custom sol() function callable

        specify a,g constants experimentally
        """

        self.bats = bats
        self.average_loudness = calculate_average_loudness(bats)
        self.fmin, self.fmax = freq_range

        for b in bats:
            b.frequency = self.fmin + (self.fmax - self.fmin)*random.random()
            b.position = df[0] + (df[1]-df[0])*random.random()
            b.loudness = random.uniform(0,1)

        bat = bats[random.randint(0, len(bats)-1)]
        self.gbest = (bat.position, sol(bat.position))
        self.pbest = (bat.position, sol(bat.position))
        self.sol = sol
        self.a = a
        self.g = g
        self.step = 0
        self.df = df


    def move_bat(self, bat, distance):
        if bat.position + distance < self.df[1] and \
                bat.position + distance > self.df[0]:
            bat.position += distance
            return True
        return None

    def update_velocity(self):
        for bat in self.bats:
            b = random.uniform(0,1.0)
            f_i = self.fmin+(self.fmax-self.fmin)*b
            phi = random.uniform(0,0.3)
            phi2= random.uniform(0,0.6)
            bat.velocity = bat.pulse_rate*bat.velocity + (self.gbest[0]-bat.position)*self.average_loudness
            #bat.velocity = bat.pulse_rate*bat.velocity+phi*(self.pbest[0]-bat.position)+phi2*(self.gbest[0]-bat.position)

    def move_bats(self):
        for bat in self.bats:
            if not self.move_bat(bat, bat.velocity):
                bat.velocity = -1*bat.velocity

    def evaluate(self):
        r = random.uniform(0,1)

        for bat in self.bats:
                # wybor rozwiazania sposrod najlepszych (?)
                # generowanie lokalnego rozwiazania wokol wybranych najlepszych (?)
                #b = random.uniform(0,1)
                #bat.velocity += (bat.position - self.gbest[0])*(self.fmin+(self.fmax-self.fmin)*b)
            bat.velocity = self.average_loudness*bat.velocity + (self.gbest[0]-bat.position)*bat.pulse_rate
            bat.fitness = self.sol(bat.position)

        bats = self.bats[:]
        bats.sort(lambda a,b: cmp(a.fitness, b.fitness), reverse=True)
        lbest = bats[0].position, bats[0].fitness

        for bat in self.bats:
            if bat.fitness>lbest[1]:
                # blizej rozwiazania, zwiekszamy puls, zmniejszamy glosnosc
                bat.pulse_rate = bat.initial_pulse_rate*(1-math.exp(-self.g*self.step))
                bat.loudness = self.a * bat.loudness
        
    def next(self):

        #self.update_velocity()
        self.move_bats()
        self.evaluate()

        bats = self.bats[:]
        bats.sort(lambda a,b: cmp(a.fitness, b.fitness), reverse=True)
        self.pbest = bats[0].position, self.sol(bats[0].position)

        bat = bats[0]
        bat.pulse_rate = bat.initial_pulse_rate*(1-math.exp(-self.g*self.step))
        bat.loudness = self.a * bat.loudness

        if self.pbest[1] > self.gbest[1]:
            self.gbest = self.pbest[:]
        
        # obliczenie sredniej glosnosci populacji
        self.average_loudness = calculate_average_loudness(self.bats)

        # kolejny krok
        self.step+=1


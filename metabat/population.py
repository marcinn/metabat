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
            b.loudness = random.uniform(1,2)

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
            return distance
        return None

    def update_velocity(self):
        for bat in self.bats:
            # rekord nietoperza
            #if not bat.pbest or v>bat.pbest[1]:
            #    bat.pbest = (bat.position, v)
            #v = self.sol(bat.position)
            #bat.isol = v

            #b = random.random()
            #bat.frequency = self.fmin + (self.fmax - self.fmin)*b
            bat.velocity += (bat.position - self.gbest[0])*bat.frequency
        
    def next(self):
        self.update_velocity()
        r = random.uniform(0,1)
        for bat in self.bats:
            # move bat
            if not self.move_bat(bat, bat.velocity):
                bat.velocity = -1 * bat.velocity

        for bat in self.bats:
            r = random.uniform(0,1)
            if r<bat.pulse_rate:
                # wybor rozwiazania sposrod najlepszych (?)
                # generowanie lokalnego rozwiazania wokol wybranych najlepszych (?)
                bats = self.bats[:]
                bats.sort(lambda a,b: cmp(a.pulse_rate, b.pulse_rate), reverse=True)
                bat.velocity += (bat.position - bats[0].position)*bat.frequency
            else:
                self.move_bat(bat, self.average_loudness*random.uniform(-1,1))

            r = random.uniform(0,1)
            if r<bat.loudness and self.sol(bat.position)<self.gbest[1]:
                # blizej rozwiazania, zwiekszamy puls, zmniejszamy glosnosc
                bat.pulse_rate = bat.initial_pulse_rate*(1-math.exp(-self.g*self.step))
                bat.loudness = self.a * bat.loudness

        bats = self.bats[:]
        bats.sort(lambda a,b: cmp(self.sol(a.position), self.sol(b.position)), reverse=True)
        self.pbest = bats[0].position, self.sol(bats[0].position)

        if self.pbest[1] > self.gbest[1]:
            self.gbest = self.pbest[:]
        
        #for bat in self.bats:
        #    bat.frequency = bat.pulse_rate*bat.frequency

        # obliczenie sredniej glosnosci populacji
        self.average_loudness = calculate_average_loudness(self.bats)

        # kolejny krok
        self.step+=1


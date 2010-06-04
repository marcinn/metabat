import random
import math

def calculate_average_loudness(bats):
    return sum((b.loudness for b in bats)) / len(bats)


class Population(object):
    def __init__(self, bats, freq_range, sol, a=0.9, g=0.9):
        """
        initialize population of bats
        with specified frequency range (min, max)
        and custom sol() function callable

        specify a,g constants experimentally
        """

        self.bats = bats
        self.average_loudness = calculate_average_loudness(bats)
        self.fmin, self.fmax = freq_range

        bat = bats[random.randint(0, len(bats)-1)]
        self.gbest = (bat.position, sol(bat))
        self.sol = sol
        self.a = a
        self.g = g
        self.step = 0
        
    def next(self):
        b = random.random()
        for bat in self.bats:
            bat.frequency = self.fmin + (self.fmax - self.fmin)*b
            bat.velocity = bat.velocity + (bat.position - self.gbest[0])*bat.frequency
            bat.position = bat.position + bat.velocity
            #bat.fly()

        for bat in self.bats:
            r = random.random()
            if r>bat.pulse_rate:
                # wybor rozwiazania sposrod najlepszych (?)
                # generowanie lokalnego rozwiazania wokol wybranych najlepszych (?)
                pass

            r = random.randint(*bat.loudness_range)
            if r<bat.loudness and self.sol(bat)>self.gbest[1]:
                # blizej rozwiazania, zwiekszamy puls, zmniejszamy glosnosc
                bat.pulse_rate = bat.pulse_rate*(1-math.exp(-self.g*self.step))
                bat.loudness = self.a * bat.loudness

        # znalezienie najlepszego rozwiazania
        for bat in self.bats:
            v = self.sol(bat)
            if v>self.gbest[1]:
                self.gbest = (bat.position, v)

        # obliczenie sredniej glosnosci populacji
        self.average_loudness = calculate_average_loudness(self.bats)

        # kolejny krok
        self.step+=1


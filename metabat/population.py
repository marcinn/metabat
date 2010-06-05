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
            b.loudness = random.random()+1

        bat = bats[random.randint(0, len(bats)-1)]
        self.gbest = (bat.position, sol(bat.position))
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
        
    def next(self):
        for bat in self.bats:
            v = self.sol(bat.position)
            # rekord nietoperza
            if not bat.pbest or v>bat.pbest[1]:
                bat.pbest = (bat.position, v)
            bat.isol = v

            b = random.random()
            #bat.frequency = self.fmin + (self.fmax - self.fmin)*b
            bat.velocity += (bat.position - self.gbest[0])*bat.frequency
            if not self.move_bat(bat, bat.velocity):
                bat.velocity = -1 * bat.velocity

        for bat in self.bats:
            r = random.random()
            if r<bat.pulse_rate:
                # wybor rozwiazania sposrod najlepszych (?)
                # generowanie lokalnego rozwiazania wokol wybranych najlepszych (?)
                """
                for friend in self.bats:
                    if friend.pulse_rate>bat.pulse_rate:
                        bat.velocity += (bat.position - friend.position)*bat.frequency
                        self.move_bat(bat, bat.velocity)
                if bat.pbest[1] < bat.isol:
                    bat.velocity = -1 * bat.velocity
                    bat.pulse_rate *= self.a
                else:
                    self.move_bat(bat, (random.random()*2-1)*self.average_loudness)
                """
                pass

            r = random.random()
            if r<bat.loudness and self.sol(bat.position)<self.gbest[1]:
                # blizej rozwiazania, zwiekszamy puls, zmniejszamy glosnosc
                bat.pulse_rate = bat.initial_pulse_rate*(1-math.exp(-self.g*self.step))
                bat.loudness = self.a * bat.loudness

        # znalezienie najlepszego rozwiazania
        for bat in self.bats:
            # najlepszy wynik populacji
            if bat.pbest[1]>self.gbest[1]:
                self.gbest = bat.pbest
        

        # obliczenie sredniej glosnosci populacji
        self.average_loudness = calculate_average_loudness(self.bats)

        # kolejny krok
        self.step+=1


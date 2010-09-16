import random

class Microbat(object):

    def __init__(self, position, velocity):
        """
        initialize micro-bat properties

        position: initial value of any comparable type 
                  with support for arithmetic operations
        velocity: initial velocity
        loudness_range: (min, max) tuple
        """

        # pulse emission rate in [0,1] range
        self.pulse_rate = random.random()
        self.initial_pulse_rate = self.pulse_rate
        self.fitness = 0

        # loudness 
        self.loudness = random.random()

        # pulse frequency
        self.frequency = random.random()/4
        
        # position
        self.position = position

        # velocity
        self.velocity = velocity

        # best result for this bat (position, value) tuple or None
        self.pbest = None


    def __repr__(self):
        return '(%s) pos=%.4f, v=%.4f, fq=%.4f, lo=%.4f, pls=%.4f, fitness=%s' % (
                self.__class__.__name__,
                self.position, self.velocity, self.frequency,
                self.loudness, self.pulse_rate, self.fitness)


def create_population(n, position_unit_vector, rndfactor=1, species=Microbat):
    """
    create population of n-bats with default position pos
    randomized in [0,radius] range
    """
    
    population = []
    for i in xrange(0, n):
        pos = position_unit_vector * random.random() * rndfactor
        population.append(species(position=pos, velocity=pos*0))
    return population


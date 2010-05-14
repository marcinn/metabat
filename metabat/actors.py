import random

class Microbat(object):

    LOUDNESS_MIN = 0
    LOUDNESS_MAX = 100

    FREQUENCY_MIN = 0
    FREQUENCY_MAX = 100

    def __init__(self, position, velocity, loudness_range=None):
        """
        initialize micro-bat properties

        position: initial value of any comparable type 
                  with support for arithmetic operations
        velocity: initial velocity
        loudness_range: (min, max) tuple
        """

        # pulse emission rate in [0,1] range
        self.pulse_rate = random.random()

        # loudness 
        self.loudness_range = loudness_range or (self.LOUDNESS_MIN, 
                self.LOUDNESS_MAX)
        self._loudness = random.randint(*(self.loudness_range))

        # pulse frequency
        self._frequency = self.FREQUENCY_MIN
        
        # position
        self.position = position

        # velocity
        self.velocity = velocity


    def _set_frequency(self, freq):
        if freq<self.FREQUENCY_MIN or freq>self.FREQUENCY_MAX:
            raise ValueError('Invalid frequency')
        self._frequency = freq

    def _get_frequency(self):
        return self._frequency
    frequency = property(_get_frequency, _set_frequency)

    def _set_loudness(self, loudness):
        if loudness<self.loudness_range[0] or \
                loudness>self.loudness_range[1]:
            raise ValueError('Invalid loudness')
        self._loudness = loudness

    def _get_loudness(self):
        return self._loudness
    loudness = property(_get_loudness, _set_loudness)

    def fly(self):
        """
        recalculate
        calculate new position and move
        Xt = Xt-1 + Vt
        """
        self.position = self.position + self.velocity

    def __repr__(self):
        return '(%s) x=%s, v=%s, f=%s, l=%s, p=%s' % (
                self.__class__.__name__,
                self.position, self.velocity, self._frequency,
                self._loudness, self.pulse_rate)


def create_population(n, initial_position, species=Microbat):
    """
    create population of n-bats with default position pos
    randomized in [0,radius] range
    """

    return [species(position=initial_position, velocity=initial_position*0) \
            for i in xrange(0, n)]


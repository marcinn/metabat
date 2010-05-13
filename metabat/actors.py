

class Microbat(object):

    LOUDNESS_MIN = 0
    LOUDNESS_MAX = 100

    MAX_FREQUENCY = 10000

    def __init__(self, position, velocity, loudness_range=None):
        """
        initialize micro-bat properties

        position: initial value of any comparable type 
                  with support for arithmetic operations
        velocity: initial velocity
        loudness_range: (min, max) tuple
        """

        # pulse emission rate in [0,1] range
        self.pulse_rate = 0.0

        # loudness 
        self.loudness_range = loudness_range or (self.LOUDNESS_MIN, 
                self.LOUDNESS_MAX)
        self._loudness = self.loudness_range[0] # min loudness at init

        # pulse frequency
        self._frequency = 0
        
        # position
        self.position = position

        # velocity
        self.velocity = velocity


    def _set_frequency(self, freq):
        if freq<0 or freq>self.MAX_FREQUENCY:
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


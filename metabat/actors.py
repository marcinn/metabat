

class Microbat(object):

    LOUDNESS_MIN = 0
    LOUDNESS_MAX = 100

    MAX_FREQUENCY = 10000

    def __init__(self, loudness_range=None):
        """
        initialize micro-bat properties

        loudness_range: (min, max) tuple
        """

        # pulse emission rate in [0,1] range
        self.pulse_rate = 0.0

        # loudness 
        self.loudness_range = loudness_range or (self.LOUDNESS_MIN, 
                self.LOUDNESS_MAX)
        self.loudness = self.loudness_range[0] # min loudness at init

        # pulse frequency
        self._frequency = 0
        

    def _set_frequency(self, freq):
        if freq<0 or freq>self.MAX_FREQUENCY:
            raise ValueError('Invalid frequency')
        self._frequency = freq

    def _get_frequency(self):
        return self._frequency

    frequency = property(_get_frequency, _set_frequency)


